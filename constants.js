const configObj = {};

const defaultConfig = {
  PORT: process.env.PORT || 9001
};

export default {
  ...defaultConfig,
  ...configObj
};
