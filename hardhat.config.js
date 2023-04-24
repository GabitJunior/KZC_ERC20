require("@nomicfoundation/hardhat-toolbox");
require("@nomiclabs/hardhat-etherscan");
require("dotenv").config();

const bnbt_priv = process.env.bnbt_priv_key;
const bnbt_rpc_url = process.env.bnbt_rpc_url;
const ETHERSCAN_API_KEY = process.env.ETHERSCAN_API_KEY;

module.exports = {
  defaultNetwork: "hardhat",
  networks: {
    bnbt:{
      url: bnbt_rpc_url,
      accounts: [bnbt_priv],
      chainId: 97
    },
  },
  etherscan: {
    apiKey: ETHERSCAN_API_KEY,
  }, 
  solidity: "0.8.18",
};
