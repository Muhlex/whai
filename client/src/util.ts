export type Recorder = {
	start: () => void,
	stop: () => Promise<{ blob: Blob }>
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
							resolve({ blob });
						};

						mediaRecorder.stop();
					});
				};

				resolve({ start, stop: stop as Recorder["stop"] });
			});
	});
};
