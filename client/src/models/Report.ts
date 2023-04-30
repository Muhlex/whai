import Reactive from "./Reactive";

let reportID = 0;
const getNextReportID = () => reportID++;

export type Entry = {
	text: string,
	status?: "pending" | "success" | "error",
}

export class Report extends Reactive {
	id: number;
	title: string;
	date: Date;
	location?: string;
	problem: Entry[];
	solution: Entry[];

	constructor(options: Partial<Report> = {}) {
		super();
		this.title = "Untitled Report";
		this.date = new Date();
		this.problem = [];
		this.solution = [];
		Object.assign(this, options);

		this.id = getNextReportID();
	}

	static fromJSON(json: string) {
		const options = JSON.parse(json);
		options.date = new Date(options.date);
		return new Report(options);
	}

	toJSON() {
		const entryCancelStatus = (e: Entry) => ({ ...e, status: e.status === "pending" ? "error" : e.status });
		return JSON.stringify({
			...this,
			date: this.date.toISOString(),
			problem: this.problem.map(entryCancelStatus),
			solution: this.solution.map(entryCancelStatus),
		});
	}

	trim() {
		[this.problem, this.solution] = [this.problem, this.solution]
			.map(entries => entries
				.map(e => ({ text: e.text.trim(), ...e }))
				.filter(e => e.text.length > 0)
			);
		this.notify();
	}
}
