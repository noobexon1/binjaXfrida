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
            code.writeU32(raw ^ 1); // XOR with 1 in AArch64 negates conditional branching.
        });
        console.log(`\tafter: ${Instruction.parse(targetAddr)}`);
    } else {
        console.log("[!] Failed to find module");
    }
})();