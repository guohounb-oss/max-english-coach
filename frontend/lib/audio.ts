export function base64ToAudioBuffer(base64: string): AudioBuffer | null {
  // For playback, we return a Blob URL approach instead
  return null;
}

export function playAudioFromBase64(base64: string, volume: number = 1): Promise<void> {
  return new Promise((resolve, reject) => {
    const binary = atob(base64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
      bytes[i] = binary.charCodeAt(i);
    }
    const blob = new Blob([bytes], { type: "audio/mp3" });
    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);
    audio.volume = volume;

    audio.onended = () => {
      URL.revokeObjectURL(url);
      resolve();
    };

    audio.onerror = (e) => {
      URL.revokeObjectURL(url);
      reject(e);
    };

    audio.play().catch(reject);
  });
}
