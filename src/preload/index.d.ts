import { ElectronAPI } from "@electron-toolkit/preload";

declare global {
  interface Window {
    electron: ElectronAPI;
    api: {
      copyText: (text: string) => void;
      copyImage: (image: string) => void;
      saveImage: (image: string, filename: string) => void;
      readLocalFile: (fileName: string) => Promise<string>;
      writeLocalFile: (fileName: string, content: string) => Promise<boolean>;
      getWindowId: () => number;
      getWebContentsId: () => number;
      getPathForFile: (file: File) => string;
    };
    floatingButtonAPI: any;
    resetInitComplete: () => Promise<void>;
  }
}
