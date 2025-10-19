(function () {
    const moduleName = "[MODULE_NAME_PLACEHOLDER]"; 
    const condBranchRelAddr = "[RELATIVE_ADDRESS_PLACEHOLDER]";

    const module = Process.findModuleByName(moduleName);
    if (module != null) {
        const targetAddr = module.base.add(condBranchRelAddr);

        console.log(`[+] Negating conditional branch at ${targetAddr}`);
        console.log(`\tbefore: ${Instruction.parse(targetAddr)}`);

        let patchPtr;

        const firstByte = Memory.readU8(targetAddr);
        if (firstByte === 0x0F) {
            const secondByte = Memory.readU8(targetAddr.add(1));
            if ((secondByte & 0xF0) === 0x80) {
                patchPtr = targetAddr.add(1);
            }
        } else if ((firstByte & 0xF0) === 0x70) {
            patchPtr = targetAddr;
        }

        if (patchPtr) {
            Memory.patchCode(patchPtr, 1, code => {
                const raw = Memory.readU8(patchPtr);
                Memory.writeU8(code, raw ^ 1);
            })
        }

        console.log(`\tafter: ${Instruction.parse(targetAddr)}`);
    } else {
        console.log("[!] Failed to find module");
    }
})();