import Home from "./views/Home.svelte";
import Report from "./views/Report.svelte";
import NotFound from "./views/NotFound.svelte";

export default {
	"/": Home,
	"/report/:id?/:edit?" : Report,
	"*": NotFound,
}
