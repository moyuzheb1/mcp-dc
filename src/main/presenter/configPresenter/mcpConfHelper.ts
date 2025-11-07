import { eventBus, SendTarget } from "@/eventbus";
import { MCPServerConfig } from "@shared/presenter";
import { MCP_EVENTS } from "@/events";
import ElectronStore from "electron-store";
import { app } from "electron";
import { compare } from "compare-versions";
import { presenter } from "..";

// NPM Registry cache interface
export interface INpmRegistryCache {
  registry: string;
  lastChecked: number;
  isAutoDetect: boolean;
}

// MCP settings interface
interface IMcpSettings {
  mcpServers: Record<string, MCPServerConfig>;
  defaultServer?: string; // Keep old field for version compatibility
  defaultServers: string[]; // New: multiple default servers array
  mcpEnabled: boolean; // Add MCP enabled status field
  npmRegistryCache?: INpmRegistryCache; // NPM registry cache
  customNpmRegistry?: string; // User custom NPM registry
  autoDetectNpmRegistry?: boolean; // Whether to enable auto detection
  [key: string]: unknown; // Allow arbitrary keys
}
export type MCPServerType = "stdio" | "sse" | "inmemory" | "http";

// Extended MCP server config with additional properties for ModelScope sync
export interface ExtendedMCPServerConfig {
  name: string;
  description: string;
  args: string[];
  env: Record<string, string>;
  enabled: boolean;
  type: MCPServerType;
  package?: string;
  version?: string;
  source?: string;
  logo_url?: string;
  publisher?: string;
  tags?: string[];
  view_count?: number;
}

// Check current system platform
function isMacOS(): boolean {
  return process.platform === "darwin";
}

function isWindows(): boolean {
  return process.platform === "win32";
}

function isLinux(): boolean {
  return process.platform === "linux";
}

// Platform-specific MCP server configurations
const PLATFORM_SPECIFIC_SERVERS: Record<string, MCPServerConfig> = {
  // macOS specific services
  ...(isMacOS()
    ? {
        "deepchat/apple-server": {
          args: [],
          descriptions: "DeepChat内置Apple系统集成服务 (仅macOS)",
          icons: "🍎",
          autoApprove: ["all"],
          type: "inmemory" as MCPServerType,
          command: "deepchat/apple-server",
          env: {},
          disable: false,
        },
      }
    : {}),

  // Windows specific services (reserved)
  ...(isWindows()
    ? {
        // 'deepchat-inmemory/windows-server': {
        //   args: [],
        //   descriptions: 'DeepChat built-in Windows system integration service (Windows only)',
        //   icons: '🪟',
        //   autoApprove: ['all'],
        //   type: 'inmemory' as MCPServerType,
        //   command: 'deepchat-inmemory/windows-server',
        //   env: {},
        //   disable: false
        // }
      }
    : {}),

  // Linux specific services (reserved)
  ...(isLinux()
    ? {
        // 'deepchat-inmemory/linux-server': {
        //   args: [],
        //   descriptions: 'DeepChat built-in Linux system integration service (Linux only)',
        //   icons: '🐧',
        //   autoApprove: ['all'],
        //   type: 'inmemory' as MCPServerType,
        //   command: 'deepchat-inmemory/linux-server',
        //   env: {},
        //   disable: false
        // }
      }
    : {}),
};

// Extract inmemory type services as constants
const DEFAULT_INMEMORY_SERVERS: Record<string, MCPServerConfig> = {
  buildInFileSystem: {
    args: [app.getPath("home")],
    descriptions: "DeepChat内置文件系统mcp服务",
    icons: "📁",
    autoApprove: ["read"],
    type: "inmemory" as MCPServerType,
    command: "filesystem",
    env: {},
    disable: true,
  },
};

const DEFAULT_MCP_SERVERS = {
  mcpServers: {
    // First define built-in MCP servers
    ...DEFAULT_INMEMORY_SERVERS,
    // All other MCP servers have been removed
  },
  defaultServers: [
    // 只保留文件系统服务，不设置为默认启用
  ],
  mcpEnabled: false, // MCP functionality is disabled by default
};
// This part of MCP has system logic to determine whether to enable, not controlled by user configuration, but by software environment
export const SYSTEM_INMEM_MCP_SERVERS: Record<string, MCPServerConfig> = {
  // custom-prompts-server has been removed, now provides prompt functionality through config data source
};

export class McpConfHelper {
  private mcpStore: ElectronStore<IMcpSettings>;

  constructor() {
    // Initialize MCP settings storage
    this.mcpStore = new ElectronStore<IMcpSettings>({
      name: "mcp-settings",
      defaults: {
        mcpServers: DEFAULT_MCP_SERVERS.mcpServers,
        defaultServers: DEFAULT_MCP_SERVERS.defaultServers,
        mcpEnabled: DEFAULT_MCP_SERVERS.mcpEnabled,
        autoDetectNpmRegistry: true,
        npmRegistryCache: undefined,
        customNpmRegistry: undefined,
      },
    });
  }

  // Get MCP server configuration
  async getMcpServers(): Promise<Record<string, MCPServerConfig>> {
    // 只返回默认的文件系统服务，忽略任何存储的旧配置
    // 这确保了即使有旧配置，也只会显示文件系统服务
    return DEFAULT_MCP_SERVERS.mcpServers;
  }

  // 设置MCP服务器配置
  async setMcpServers(servers: Record<string, MCPServerConfig>): Promise<void> {
    this.mcpStore.set("mcpServers", servers);
    eventBus.send(MCP_EVENTS.CONFIG_CHANGED, SendTarget.ALL_WINDOWS, {
      mcpServers: servers,
      defaultServers: this.mcpStore.get("defaultServers") || [],
      mcpEnabled: this.mcpStore.get("mcpEnabled"),
    });
  }

  // 获取默认服务器列表
  getMcpDefaultServers(): Promise<string[]> {
    return Promise.resolve(this.mcpStore.get("defaultServers") || []);
  }

  // 添加默认服务器
  async addMcpDefaultServer(serverName: string): Promise<void> {
    const defaultServers = this.mcpStore.get("defaultServers") || [];
    const mcpServers = await this.getMcpServers(); // 使用getMcpServers确保平台检查

    // 检测并清理失效的服务器
    const validDefaultServers = defaultServers.filter((server) => {
      const exists = mcpServers[server] !== undefined;
      if (!exists) {
        console.log(
          `Detected invalid MCP server: ${server}, removed from default list`,
        );
      }
      return exists;
    });

    // 检查要添加的服务器是否存在且支持当前平台
    if (mcpServers[serverName]) {
      // 添加新服务器（如果不在列表中）
      if (!validDefaultServers.includes(serverName)) {
        validDefaultServers.push(serverName);
      }
    } else {
      console.log(
        `Attempted to add non-existent or unsupported MCP server for current platform: ${serverName}`,
      );
      return;
    }

    // 如果有变化则更新存储并发送事件
    if (
      validDefaultServers.length !== defaultServers.length ||
      !defaultServers.includes(serverName)
    ) {
      this.mcpStore.set("defaultServers", validDefaultServers);
      eventBus.send(MCP_EVENTS.CONFIG_CHANGED, SendTarget.ALL_WINDOWS, {
        mcpServers: mcpServers,
        defaultServers: validDefaultServers,
        mcpEnabled: this.mcpStore.get("mcpEnabled"),
      });
    }
  }

  // 移除默认服务器
  async removeMcpDefaultServer(serverName: string): Promise<void> {
    const defaultServers = this.mcpStore.get("defaultServers") || [];
    const updatedServers = defaultServers.filter((name) => name !== serverName);
    this.mcpStore.set("defaultServers", updatedServers);
    eventBus.send(MCP_EVENTS.CONFIG_CHANGED, SendTarget.ALL_WINDOWS, {
      mcpServers: this.mcpStore.get("mcpServers"),
      defaultServers: updatedServers,
      mcpEnabled: this.mcpStore.get("mcpEnabled"),
    });
  }

  // 切换服务器的默认状态
  async toggleMcpDefaultServer(serverName: string): Promise<void> {
    const defaultServers = this.mcpStore.get("defaultServers") || [];
    if (defaultServers.includes(serverName)) {
      await this.removeMcpDefaultServer(serverName);
    } else {
      await this.addMcpDefaultServer(serverName);
    }
  }

  // 设置MCP启用状态
  async setMcpEnabled(enabled: boolean): Promise<void> {
    this.mcpStore.set("mcpEnabled", enabled);
    eventBus.send(MCP_EVENTS.CONFIG_CHANGED, SendTarget.ALL_WINDOWS, {
      mcpServers: this.mcpStore.get("mcpServers"),
      defaultServers: this.mcpStore.get("defaultServers"),
      mcpEnabled: enabled,
    });
  }

  // 获取MCP启用状态
  getMcpEnabled(): Promise<boolean> {
    return Promise.resolve(
      this.mcpStore.get("mcpEnabled") ?? DEFAULT_MCP_SERVERS.mcpEnabled,
    );
  }

  // 添加MCP服务器
  async addMcpServer(name: string, config: MCPServerConfig): Promise<boolean> {
    const mcpServers = await this.getMcpServers();
    mcpServers[name] = config;
    await this.setMcpServers(mcpServers);
    return true;
  }

  // 获取NPM Registry缓存
  getNpmRegistryCache(): INpmRegistryCache | undefined {
    return this.mcpStore.get("npmRegistryCache");
  }

  // 设置NPM Registry缓存
  setNpmRegistryCache(cache: INpmRegistryCache): void {
    this.mcpStore.set("npmRegistryCache", cache);
  }

  // 检查缓存是否有效（24小时内）
  isNpmRegistryCacheValid(): boolean {
    const cache = this.getNpmRegistryCache();
    if (!cache) return false;
    const now = Date.now();
    const cacheAge = now - cache.lastChecked;
    const CACHE_DURATION = 24 * 60 * 60 * 1000; // 24小时
    return cacheAge < CACHE_DURATION;
  }

  // 获取有效的NPM Registry（按优先级：自定义源 > 缓存 > 默认）
  getEffectiveNpmRegistry(): string | null {
    const customRegistry = this.getCustomNpmRegistry();
    if (customRegistry) {
      console.log(`[NPM Registry] Using custom registry: ${customRegistry}`);
      return customRegistry;
    }

    if (this.getAutoDetectNpmRegistry() && this.isNpmRegistryCacheValid()) {
      const cache = this.getNpmRegistryCache();
      if (cache?.registry) {
        console.log(`[NPM Registry] Using cached registry: ${cache.registry}`);
        return cache.registry;
      }
    }

    console.log(
      "[NPM Registry] No effective registry found, will use default or detect",
    );
    return null;
  }

  // 获取自定义NPM Registry
  getCustomNpmRegistry(): string | undefined {
    return this.mcpStore.get("customNpmRegistry");
  }

  // 标准化NPM Registry URL
  private normalizeNpmRegistryUrl(registry: string): string {
    let normalized = registry.trim();
    if (!normalized.endsWith("/")) {
      normalized += "/";
    }
    return normalized;
  }

  // 设置自定义NPM Registry
  setCustomNpmRegistry(registry: string | undefined): void {
    if (registry === undefined) {
      this.mcpStore.delete("customNpmRegistry");
    } else {
      const normalizedRegistry = this.normalizeNpmRegistryUrl(registry);
      this.mcpStore.set("customNpmRegistry", normalizedRegistry);
      console.log(
        `[NPM Registry] Normalized custom registry: ${registry} -> ${normalizedRegistry}`,
      );
    }
  }

  // 获取自动检测NPM Registry设置
  getAutoDetectNpmRegistry(): boolean {
    return this.mcpStore.get("autoDetectNpmRegistry") ?? true;
  }

  // 设置自动检测NPM Registry
  setAutoDetectNpmRegistry(enabled: boolean): void {
    this.mcpStore.set("autoDetectNpmRegistry", enabled);
  }

  // 清除NPM Registry缓存
  clearNpmRegistryCache(): void {
    this.mcpStore.delete("npmRegistryCache");
  }

  // 移除MCP服务器
  async removeMcpServer(name: string): Promise<void> {
    const mcpServers = await this.getMcpServers();
    delete mcpServers[name];
    await this.setMcpServers(mcpServers);

    // 如果删除的服务器在默认服务器列表中，则从列表中移除
    const defaultServers = await this.getMcpDefaultServers();
    if (defaultServers.includes(name)) {
      await this.removeMcpDefaultServer(name);
    }
  }

  // 更新MCP服务器配置
  async updateMcpServer(
    name: string,
    config: Partial<MCPServerConfig>,
  ): Promise<void> {
    const mcpServers = await this.getMcpServers();
    if (!mcpServers[name]) {
      throw new Error(`MCP server ${name} not found`);
    }
    mcpServers[name] = {
      ...mcpServers[name],
      ...config,
    };
    await this.setMcpServers(mcpServers);
  }

  // 恢复默认服务器配置
  async resetToDefaultServers(): Promise<void> {
    // 直接使用默认服务器配置，只保留文件系统服务
    await this.setMcpServers(DEFAULT_MCP_SERVERS.mcpServers);

    // 恢复默认服务器设置，确保平台特有服务的正确处理
    const platformAwareDefaultServers = [
      // 只保留文件系统服务，不设置为默认启用
    ];

    this.mcpStore.set("defaultServers", platformAwareDefaultServers);
    eventBus.send(MCP_EVENTS.CONFIG_CHANGED, SendTarget.ALL_WINDOWS, {
      mcpServers: DEFAULT_MCP_SERVERS.mcpServers,
      defaultServers: platformAwareDefaultServers,
      mcpEnabled: this.mcpStore.get("mcpEnabled"),
    });
  }

  /**
   * Batch import MCP servers from external source (like ModelScope)
   * @param servers - Array of MCP server configs to import
   * @param options - Import options
   * @returns Promise<{ imported: number; skipped: number; errors: string[] }>
   */
  async batchImportMcpServers(
    servers: Array<{
      name: string;
      description: string;
      package: string;
      version?: string;
      type?: MCPServerType;
      args?: string[];
      env?: Record<string, string>;
      enabled?: boolean;
      source?: string;
      [key: string]: unknown;
    }>,
    options: {
      skipExisting?: boolean;
      enableByDefault?: boolean;
      overwriteExisting?: boolean;
    } = {},
  ): Promise<{ imported: number; skipped: number; errors: string[] }> {
    const {
      skipExisting = true,
      enableByDefault = false,
      overwriteExisting = false,
    } = options;
    const result = {
      imported: 0,
      skipped: 0,
      errors: [] as string[],
    };

    const existingServers = await this.getMcpServers();

    for (const serverConfig of servers) {
      try {
        // Generate unique server name based on package name
        const serverName = this.generateUniqueServerName(
          serverConfig.package,
          existingServers,
        );
        const existingServer = existingServers[serverName];

        // Check if server already exists
        if (existingServer && !overwriteExisting) {
          if (skipExisting) {
            console.log(`Skipping existing MCP server: ${serverName}`);
            result.skipped++;
            continue;
          } else {
            result.errors.push(`Server ${serverName} already exists`);
            continue;
          }
        }

        // Create MCP server config
        const mcpConfig: ExtendedMCPServerConfig = {
          name: serverConfig.name,
          description: serverConfig.description,
          args: serverConfig.args || [],
          env: serverConfig.env || {},
          enabled: serverConfig.enabled ?? enableByDefault,
          type: (serverConfig.type as MCPServerType) || "stdio",
          package: serverConfig.package,
          version: serverConfig.version || "latest",
          source: serverConfig.source as string | undefined,
          logo_url: serverConfig.logo_url as string | undefined,
          publisher: serverConfig.publisher as string | undefined,
          tags: serverConfig.tags as string[] | undefined,
          view_count: serverConfig.view_count as number | undefined,
        };

        // Add or update the server
        const success = await this.addMcpServer(
          serverName,
          mcpConfig as unknown as MCPServerConfig,
        );
        if (success || overwriteExisting) {
          if (existingServer && overwriteExisting) {
            await this.updateMcpServer(
              serverName,
              mcpConfig as unknown as Partial<MCPServerConfig>,
            );
            console.log(`Updated MCP server: ${serverName}`);
          } else {
            console.log(`Imported MCP server: ${serverName}`);
          }
          result.imported++;
        } else {
          result.errors.push(`Failed to import server: ${serverName}`);
        }
      } catch (error) {
        const errorMsg = `Error importing server ${serverConfig.name}: ${error instanceof Error ? error.message : String(error)}`;
        console.error(errorMsg);
        result.errors.push(errorMsg);
      }
    }

    console.log(
      `MCP batch import completed. Imported: ${result.imported}, Skipped: ${result.skipped}, Errors: ${result.errors.length}`,
    );

    // Emit event to notify about the import
    eventBus.sendToRenderer(MCP_EVENTS.CONFIG_CHANGED, SendTarget.ALL_WINDOWS, {
      action: "batch_import",
      result,
    });

    return result;
  }

  /**
   * Generate a unique server name based on package name
   * @param packageName - The package name to base the server name on
   * @param existingServers - Existing servers to check against
   * @returns Unique server name
   */
  private generateUniqueServerName(
    packageName: string,
    existingServers: Record<string, MCPServerConfig>,
  ): string {
    // Clean up package name to create a suitable server name
    let baseName = packageName
      .replace(/[@/]/g, "-")
      .replace(/[^a-zA-Z0-9-_]/g, "")
      .toLowerCase();

    // If the base name doesn't exist, use it directly
    if (!existingServers[baseName]) {
      return baseName;
    }

    // If it exists, append a number suffix
    let counter = 1;
    let uniqueName = `${baseName}-${counter}`;
    while (existingServers[uniqueName]) {
      counter++;
      uniqueName = `${baseName}-${counter}`;
    }

    return uniqueName;
  }

  /**
   * Check if a server with given package already exists
   * @param packageName - Package name to check
   * @returns Promise<string | null> - Returns server name if exists, null otherwise
   */
  async findServerByPackage(packageName: string): Promise<string | null> {
    const servers = await this.getMcpServers();

    for (const [serverName, config] of Object.entries(servers)) {
      const extendedConfig = config as unknown as ExtendedMCPServerConfig;
      if (extendedConfig.package === packageName) {
        return serverName;
      }
    }

    return null;
  }

  public onUpgrade(oldVersion: string | undefined): void {
    console.log("onUpgrade", oldVersion);

    // 清理MCP配置，只保留文件系统服务
    console.log(
      "Cleaning up MCP configuration, keeping only filesystem service",
    );
    const mcpServers = { ...DEFAULT_MCP_SERVERS.mcpServers };
    this.mcpStore.set("mcpServers", mcpServers);
    this.mcpStore.set("defaultServers", []);

    // 确保不加载任何平台特有服务
    console.log("Ensuring no platform-specific services are loaded");

    // 发送配置更改事件
    eventBus.send(MCP_EVENTS.CONFIG_CHANGED, SendTarget.ALL_WINDOWS, {
      mcpServers: mcpServers,
      defaultServers: [],
      mcpEnabled: this.mcpStore.get("mcpEnabled"),
    });
  }
}
