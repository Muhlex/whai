import Home from "./views/Home.svelte";
import Intro from "./views/Intro.svelte";
import Report from "./views/Report.svelte";
import Settings from "./views/Settings.svelte";
import NotFound from "./views/NotFound.svelte";

export default {
	"/": Home,
	"/intro": Intro,
	"/report/:id?/:edit?" : Report,
	"/settings" : Settings,
	"*": NotFound,
}
