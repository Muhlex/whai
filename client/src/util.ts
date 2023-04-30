export type Recorder = {
	start: () => void,
	stop: () => Promise<{ blob: Blob, url: string, play: () => Promise<void> }>
};

export const recordAudio = (): Promise<Recorder> => {
	return new Promise(resolve => {
		navigator.mediaDevices.getUserMedia({ audio: true })
			.then(stream => {
				const mediaRecorder = new MediaRecorder(stream);
				const audioChunks: Blob[] = [];

				mediaRecorder.ondataavailable = event => {
					audioChunks.push(event.data);
				};

				const start = () => {
					mediaRecorder.start();
				};

				const stop = () => {
					return new Promise(resolve => {
						mediaRecorder.onstop = () => {
							const blob = new Blob(audioChunks);
							const url = URL.createObjectURL(blob);
							const audio = new Audio(url);
							const play = () => audio.play();
							resolve({ blob, url, play });
						};

						mediaRecorder.stop();
					});
				};

				resolve({ start, stop: stop as Recorder["stop"] });
			});
	});
};
