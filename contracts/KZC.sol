// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract KZC is ERC20 {
    constructor() ERC20("KZC wrapped", "KZC") {}

    function mint(address addr, uint256 amount) external {
        _mint(addr, amount);
    }

    function decimals() public view virtual override returns (uint8) {
        return 8;
    }
}