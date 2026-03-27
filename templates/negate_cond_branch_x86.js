(function () {
    const moduleName = "[MODULE_NAME_PLACEHOLDER]"; 
    const condBranchRelAddr = "[RELATIVE_ADDRESS_PLACEHOLDER]";

    const module = Process.findModuleByName(moduleName);
    if (module != null) {
        const targetAddr = module.base.add(condBranchRelAddr);

        console.log(`[+] Negating conditional branch at ${targetAddr}`);
        console.log(`\tbefore: ${Instruction.parse(targetAddr)}`);

        let patchPtr;

        const firstByte = targetAddr.readU8();
        if (firstByte === 0x0F) {
            const secondByte = targetAddr.add(1).readU8();
            if ((secondByte & 0xF0) === 0x80) {
                patchPtr = targetAddr.add(1);
            }
        } else if ((firstByte & 0xF0) === 0x70) {
            patchPtr = targetAddr;
        }

        if (patchPtr) {
            Memory.patchCode(patchPtr, 1, code => {
                const raw = patchPtr.readU8();
                code.writeU8(raw ^ 1);
            })
        }

        console.log(`\tafter: ${Instruction.parse(targetAddr)}`);
    } else {
        console.log("[!] Failed to find module");
    }
})();