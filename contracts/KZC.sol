// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract KZC is ERC20 {
    uint8 _decimals = 8;
    constructor() ERC20("KZC wrapped", "KZC") {}

    function mint(address addr, uint256 amount) external {
        require(msg.sender == address(0x00C5d1B9a29232738b5aF5028bb230519D513Da8), "You aren't the owner");
        _mint(addr, amount*10**_decimals);
    }

    function decimals() public view virtual override returns (uint8) {
        return _decimals;
    }
}