// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract KZC is ERC20 {
    uint8 _decimals = 8;
    address payable public owner;

    constructor() ERC20("KZC wrapped", "KZC") {
        owner = payable(msg.sender);
    }

    function mint(address addr, uint256 amount) external {
        require(msg.sender == owner, "You aren't the owner");
        uint256 amt_int = amount*10**_decimals;
        uint256 new_tSupply = totalSupply()*10**_decimals + amt_int;
        require(new_tSupply <= 10000, "totalSupply cannot be more than 18.9 M");

        _mint(addr, amt_int);
    }

    function decimals() public view virtual override returns (uint8) {
        return _decimals;
    }
}