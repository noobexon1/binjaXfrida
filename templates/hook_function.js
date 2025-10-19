(function () {
    const moduleName = "[MODULE_NAME_PLACEHOLDER]"; 
    const functionRelativeAddress = "[FUNCTION_RELATIVE_ADDRESS_PLACEHOLDER]";
    const functionName = "[FUNCTION_NAME_PLACEHOLDER]";

    const module = Process.findModuleByName(moduleName);
    if (module != null) {
        const targetAddr = module.base.add(functionRelativeAddress);
        console.log(`[+] Hook installed for [${functionName}]`);
        Interceptor.attach(targetAddr, {
            onEnter: function (args) { 
                console.log(`-> enetered [${functionName}] at [${targetAddr}]`);

                // Your code goes here...

            }, 
            onLeave: function (retval) {
                console.log(`<- leaving [${functionName}] at [${this.context.pc}]`);
                
                // Your code goes here...

            }
        });   
    } else {
        console.log("[!] Failed to find module");
    }
})(); 