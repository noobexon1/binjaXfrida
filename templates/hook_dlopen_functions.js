(function () {
    const moduleName = "[MODULE_NAME_PLACEHOLDER]"; 

    function hookOnLibraryLoad(dlopenFunctionAddr) {
        Interceptor.attach(dlopenFunctionAddr, {
            onEnter: function (args) {
                const loadPath = args[0].readCString();
                if (loadPath != null && loadPath.includes(moduleName)) {
                    this.isTarget = true;
                }
            },
            onLeave: function () {
                if (this.isTarget) {
                    console.log(`[+] ${moduleName} loaded!`);

                    // ** Your code goes in here... **

                    this.isTarget = false;
                }
            }
        });
    } 

    const dlopenFunctions = ["dlopen", "android_dlopen_ext"];
    for (let i = 0; i < dlopenFunctions.length; i++) {
        const address = Module.getGlobalExportByName(dlopenFunctions[i]);
        if (address != null) {
            hookOnLibraryLoad(address);
        }
    }
    
})();