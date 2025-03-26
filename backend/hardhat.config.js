require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.28",
  path:{
    artifacts: "./artifacts",
    sources: "./contracts"
  },
  optimizer: {
    enabled: true,
    runs: 200
  }
};
