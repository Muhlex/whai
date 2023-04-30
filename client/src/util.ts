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

export const shuffleArray = <T>(array: T[]) => {
	for (let i = array.length - 1; i > 0; i--) {
		const j = Math.floor(Math.random() * (i + 1));
		const temp = array[i];
		array[i] = array[j];
		array[j] = temp;
	}
	return array;
}
