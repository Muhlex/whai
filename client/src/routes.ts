import Home from "./views/Home.svelte";
import Report from "./views/Report.svelte";
import Settings from "./views/Settings.svelte";
import NotFound from "./views/NotFound.svelte";

export default {
	"/": Home,
	"/report/:id?/:edit?" : Report,
	"/settings" : Settings,
	"*": NotFound,
}
