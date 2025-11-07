import { FileSystemServer } from "./filesystem";

export function getInMemoryServer(
  serverName: string,
  args: string[],
  env?: Record<string, unknown>,
) {
  switch (serverName) {
    case "buildInFileSystem":
      return new FileSystemServer(args);
    default:
      throw new Error(`Unknown in-memory server: ${serverName}`);
  }
}
