import { writable } from "svelte/store";
import { Report } from "./models/Report";
import mockReports from "./assets/mock-reports";

export const user = writable({ name: 'Uwe Bagger' });


const reportsMap = new Map<number, Report>();
export const reports = writable(reportsMap);

export const createReport = (options?: Partial<Report>) => {
	const report = new Report(options);
	reportsMap.set(report.id, report);
	reports.update(value => value);
	return report;
};

mockReports.forEach(createReport);
