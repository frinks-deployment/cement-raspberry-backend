const configObj = {};

const defaultConfig = {
  PORT: process.env.PORT || 9000,
};

export default {
  ...defaultConfig,
  ...configObj
};
