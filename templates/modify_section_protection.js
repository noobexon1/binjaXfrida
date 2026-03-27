(function () {
    const moduleName = "[MODULE_NAME_PLACEHOLDER]"; 
    const sectionName = "[SECTION_NAME_PLACEHOLDER]";

    const module = Process.findModuleByName(moduleName);
    if (module != null) {
        let target;

        const sections = module.enumerateSections()
        for (let i = 0; i < sections.length; i++) {
            const section = sections[i];
            if (section.name == sectionName) {
                target = section;
                break;
            }
        }

        if (target) {
            const newPrermissions = 'rwx' // <-------- ** CHANGE THIS ACCORDING TO YOUR NEEDS **

            console.log(`[+] Found section [${target.name}] at ${target.address}. size: ${target.size} (bytes)`);
            console.log(`\tAttempting to change permissions from [${Memory.queryProtection(target.address)}] to [${newPrermissions}]`);
            const protectionResult = Memory.protect(target.address, target.size, newPrermissions);
            if (protectionResult) {
                console.log(`\tSuccess! [${Memory.queryProtection(target.address)}]`);
            } else {
                console.log(`[!] Failed to change memory protection`);
            }
        } else {
            console.log(`[!] Failed to find section ${sectionName}`);
        }

    } else {
        console.log("[!] Failed to find module");
    }
})();
