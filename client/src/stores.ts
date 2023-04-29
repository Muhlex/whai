import { writable } from "svelte/store";
import { Report } from "./models/Report";
import mockReports from "./assets/mock-reports";

export const languages = {
	"ar-SA": "Arabic",
	"bn-BD": "Bangla",
	"cs-CZ": "Czech",
	"da-DK": "Danish",
	"de-DE": "German",
	"el-GR": "Greek",
	"en-US": "English",
	"es-ES": "Spanish",
	"fi-FI": "Finnish",
	"fr-FR": "French",
	"he-IL": "Hebrew",
	"hi-IN": "Hindi",
	"hu-HU": "Hungarian",
	"id-ID": "Indonesian",
	"it-IT": "Italian",
	"ja-JP": "Japanese",
	"ko-KR": "Korean",
	"nl-NL": "Dutch",
	"no-NO": "Norwegian",
	"pl-PL": "Polish",
	"pt-PT": "Portugese",
	"ro-RO": "Romanian",
	"ru-RU": "Russian",
	"sk-SK": "Slovak",
	"sv-SE": "Swedish",
	"ta-IN": "Tamil",
	"th-TH": "Thai",
	"tr-TR": "Turkish",
	"zh-CN": "Chinese",
};

type UserSettings = {
	name: string,
	languages: (keyof typeof languages)[],
}
export const user = writable<UserSettings>({ name: '', languages: ["en-US", "de-DE"] });
export const introDone = writable(Boolean(localStorage.getItem("introDone")));
introDone.subscribe(done => {
	const key = "introDone";
	done ? localStorage.setItem(key, "true") : localStorage.removeItem(key);
});

const reportsMap = new Map<number, Report>();
export const reports = writable(reportsMap);

export const createReport = (options?: Partial<Report>) => {
	const report = new Report(options);
	reportsMap.set(report.id, report);
	reports.update(value => value);
	return report;
};

mockReports.forEach(createReport);
