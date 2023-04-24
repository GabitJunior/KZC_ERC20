require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

const bnbt_priv = process.env.bnbt_priv_key;
const bnbt_rpc_url = process.env.bnbt_rpc_url;

module.exports = {
  defaultNetwork: "hardhat",
  networks: {
    bnbt:{
      url: bnbt_rpc_url,
      accounts: [bnbt_priv],
      chainId: 97
    },
  },
  solidity: "0.8.18",
};
