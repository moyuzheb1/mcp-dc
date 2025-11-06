import { ElectronAPI } from '@electron-toolkit/preload'

declare global {
  interface Window {
    electron: ElectronAPI
    api: {
      copyText: (text: string) => void;
      copyImage: (image: string) => void;
      saveImage: (image: string, filename: string) => void;
      readLocalFile: (fileName: string) => Promise<string>;
    };
    floatingButtonAPI: any;
  }
}
