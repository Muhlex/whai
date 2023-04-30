export default [{
	title: "Safety inspection turbine No. 456",
	date: new Date(),
	location: "TUM Garching",
	problem: [
		"The purpose of this intervention is to adjust the bearings and twist torque on both levele of the HQM"
	],
	solution: [
		`Today I worked on several tasks related to the production and maintenance of the IBC. I helped with fixing the IBC motor\
		failure, which was caused by the web not being pulled up properly. I fixed this by changing the IBC correction value from\
		15 to 20. Then I released the torque on HQ1 and reseated the upper and lower blades. I also adjusted the HQ1 bearings\
		and the twist torque to optimize the cutting of dry 42# liner.`,
		`I secured the twisting flange fixing bolts with 650Nm of torque. I repeated the same process for HQ2, but also tuned it\
		with wet 42# liner. I tuned HQ1 with wet 42# liner as well.\
		I checked the zero pulse on both levels and found no issues. I ran HQM in test mode with a 840mm cut off at 1000fpm\
		for an hour and it worked fine. The BHS electrician replaced the drive for HQ1 because it was faulty at higher speeds. I\
		checked the bearing temperatures and they were all within spec. I checked the brake function of the medium and top\
		liner roll stand with Scott.`,
		`I also helped change out some bad clean out fingers on C flute. At 10pm, I came back to\
		monitor the production and check the cut quality and everything was running smoothly.`
	]
}, {
	title: "Splicer Issues [A3202859]",
	date: new Date("2023-04-27T10:26:47Z"),
	location: "LMU Geschw.-Scholl-Pl. 1",
	problem: ["Customer is having splicer issues on LS0. The accelerator roll is not running in thread up or during production."],
	solution: [
		`Adjusted the forward proximity switch to ensure that the dancer could calibrate and calibrated. Tested the roll drive\
		system and found the drive 1011t1 was intermittently faulting. The wires had a bad connection that terminate for\
		control. Corrected this and found that the drive would enable and was ready to run but was missing the signal. Reached\
		out to Germany for assistance and found that the drive had an issue. The speed was calculating but the drive never\
		transfered it to run.`,
		`Replaced the drive, memory module and communications card. Reloaded the parameters into the\
		drive and corrected the problem. There is some tape on the splicer roll that needs to be removed by the crew next PM.\
		The clamp bar on both sides have damage from the missed splices. The machine was not picking up the speed of the\
		paper and was calculating everything at 0 speed. This cause excessive ware on the clamping bar. The customer ordered\
		this and should replace it as soon as possible. The customer is also telling me that the roll stand 5 arms are bleeding\
		down when not running for a while. I do not trust myself to adjust the check valve to correct this issue as I am not\
		knowledgeable enough with hydraulics. I suggest to have a mechanic come to help correct this issue or attempt it with\
		the maintenance department.`
	],
}, {
	title: "Splicer Issues [A3202859]",
	date: new Date("2023-03-14T10:26:47Z"),
	location: "Ebersberg, Bayern",
	problem: ["The customer is having gap issues with MF2."],
	solution: [
		`There are many issues with the machine. The main issue for the gap is that the glue pan is bent. The cam followers are\
		also worn out and not rolling anymore along with the rails showing severe signs of wear. The customer does not have\
		the release applicator roll button on the touch screen. I sent off to Germany for an update for this on the touch screen. I\
		am not sure if this is an upgrade or not. I turned this on in the software so that the customer could run production\
		without issue. The customer replaced the rails along with the cam followers. The gap on the drive side was way off.`,
		`We calibrated electrically and the customer adjusted the mechanical stops on C-flute so that the machine is correct. B-flute\
		needs a mechanical and electrical calibration. The customer stated they are going to replace B-flute, so we did not focus\
		on this. We ran for one day with the gap control turned on and the release for the load cells turned on. Tried to push the\
		machine speed and found that the tach on the back of the main motor had water in it. This caused a major speed\
		fluctuation when the machine was pushed over 1000fpm. Cleaned with electrical contact spray, adjusted speeds on all\
		rolls on the machine and simulated production. `,
		`There is still a speed issue when running over 1000fpm.Investigated the\
		main motor and found the brushes are worn with a lot of carbon buildup inside the motor. I suggest replacing the motor\
		and send it out to have a PM performed on it. The commutator of the main motor does not show any discoloration,\
		pitting or groves. The customer should also replace the tach on the motor. There is a lot of carbon build up inside of it\
		and discoloration of the commutator. While in production, we had no issues with the gap control. I recorded the soft\
		touch and found no issues either after replacing the rails and cam followers. Placed the machine in soft touch and ran\
		over night with no issues. The customer would benefit from a mechanical tech coming in to correct mechanical issues\
		and give training. I can only go so far mechanically. Optimal path forward would be to have a mechanic come in for an\
		evaluation of the MF and give a list of parts needed to correct issues.`,
		`This would allow for a planned intervention to\
		correct the mechanical issues that the machine has along with being able to plan the down time for the intervention.\
		The limit switch for the glue pan on the drive side has issues and needs to be replaced. The maintenance guys stated\
		that it is ordered but has not come in yet. There were multiple times the glue pan would not engage due to this. The\
		applicator roll to doctor roll gap needed adjustment. The linkage is worn and needs to be replaced along with the\
		eccentrics. We could not move the gap to .006 minimum or .028 maximum. It is calibrated at .007 and .026. This should\
		be ok because only b and c flute are run on the machine and do not need the full adjustment. The lifting spindle for this\
		gap also needs to be replaced. The seal on the end of the shaft is damaged and will not stay in place allowing debris to\
		get into the gearing. It is only a matter of time before this fails.`
	],
}, {
	title: "Wind Turbines Check [#1, #2, #3, #4]",
	date: new Date("2023-01-22T10:26:47Z"),
	location: "Wind Farm Ebersberg, Bayern",
	problem: ["Wind Turbines are due for regular check-up."],
	solution: [
		"Inspected and diagnosed issue with turbine #1's gearbox",
		"Identified broken gear teeth",
		"Removed and replaced damaged gear, lubricated and reassembled gearbox",
		"Performed visual inspection of turbine #2's blades, noted minor wear and tear on several blades",
		"Used ultrasonic testing to measure blade thickness and identify potential stress points",
		"Communicated with procurement team to order replacement blades as a preventative measure",
		"Conducted regular maintenance on turbine #3's electrical system, replaced damaged wiring and cleaned components",
		"Troubleshot turbine #4's control system, identified malfunctioning sensor causing issues with automatic shutdown procedure",
		"Replaced faulty sensor and conducted system test to ensure proper functioning",
		"Updated maintenance log and completed required documentation for each turbine",
		"Communicated with team members to ensure all work was completed safely and efficiently",

	],
}];
