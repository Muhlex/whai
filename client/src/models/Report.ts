import Reactive from "./Reactive";

let reportID = 0;
const getNextReportID = () => reportID++;

export class Report extends Reactive {
	id: number;
	title: string;
	date: Date;
	location?: string;
	problem: string[];
	solution: string[];

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
		return JSON.stringify({
			...this,
			date: this.date.toISOString(),
		});
	}

	trim() {
		[this.problem, this.solution] = [this.problem, this.solution]
			.map(paras => paras.map(p => p.trim()).filter(p => p.length > 0));
		this.notify();
	}
}
