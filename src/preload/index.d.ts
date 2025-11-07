import { ElectronAPI } from "@electron-toolkit/preload";

declare global {
  interface Window {
    electron: ElectronAPI;
    api: {
      copyText: (text: string) => void;
      copyImage: (image: string) => void;
      saveImage: (image: string, filename: string) => void;
      readLocalFile: (fileName: string) => Promise<string>;
      // Additional helper methods exposed by preload
      getPathForFile: (fileName: string | File) => string;
      getWindowId: () => number;
      getWebContentsId: () => number;
    };
    floatingButtonAPI: any;
  }
}
