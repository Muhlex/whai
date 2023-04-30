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

export const introDone = writable(Boolean(localStorage.getItem("introDone")));
introDone.subscribe(done => {
	const key = "introDone";
	done ? localStorage.setItem(key, "true") : localStorage.removeItem(key);
});

type UserSettings = {
	name: string,
	language: (keyof typeof languages),
}
export const user = writable<UserSettings>(
	JSON.parse(localStorage.getItem("user")) || { name: '', language: "en-US" }
);
user.subscribe(user => {
	localStorage.setItem("user", JSON.stringify(user));
});

const reportsMap = new Map<number, Report>();
export const reports = writable(reportsMap);

export const createReport = (optionsOrJSON?: Partial<Report> | string) => {
	const report = (typeof optionsOrJSON === "string")
		?	Report.fromJSON(optionsOrJSON)
		: new Report(optionsOrJSON);
	reportsMap.set(report.id, report);
	reports.update(value => value);
	report.subscribe(() => reports.update(value => value));
	return report;
};

{
	const cachedRawReports = JSON.parse(localStorage.getItem("reports"));
	if (cachedRawReports) cachedRawReports.forEach(createReport);
	else mockReports.forEach(raw => {
		createReport({
			...raw,
			problem: raw.problem?.map(text => ({ text })) || [],
			solution: raw.solution?.map(text => ({ text })) || [],
		})
	});
}
reports.subscribe(reports => {
	const serialized = JSON.stringify([...reports.values()].map(r => r.toJSON()));
	localStorage.setItem("reports", serialized);
})
