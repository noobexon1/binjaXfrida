(function () {
    const moduleName = "[MODULE_NAME_PLACEHOLDER]"; 
    const condBranchRelAddr = "[RELATIVE_ADDRESS_PLACEHOLDER]";

    const module = Process.findModuleByName(moduleName);
    if (module != null) {
        const targetAddr = module.base.add(condBranchRelAddr);

        console.log(`[+] Negating conditional branch at ${targetAddr}`);
        console.log(`\tbefore: ${Instruction.parse(targetAddr)}`);
        Memory.patchCode(targetAddr, 4, code => {
            const raw = targetAddr.readU32();
            let xorMask;
            if ((raw & 0xFF000010) === 0x54000000) {
                xorMask = 1;            // b.cond: condition in bit 0
            } else if ((raw & 0x7E000000) === 0x36000000) {
                xorMask = 1 << 24;     // tbz/tbnz: op in bit 24
            } else if ((raw & 0x7E000000) === 0x34000000) {
                xorMask = 1 << 24;     // cbz/cbnz: op in bit 24
            } else {
                console.log("[!] Unrecognized conditional branch encoding");
                return;
            }
            code.writeU32(raw ^ xorMask);
        });
        console.log(`\tafter: ${Instruction.parse(targetAddr)}`);
    } else {
        console.log("[!] Failed to find module");
    }
})();