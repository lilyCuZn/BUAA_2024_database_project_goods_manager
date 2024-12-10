module.exports = {
  devServer: {
    proxy: {
      "/web": {
        target: "http://127.0.0.1:8000",
        // 59.110.236.209
        // 10.193.115.252
        changeOrigin: true,
        pathRewrite: {
          "^": "",
        },
      },
    },
  },
};
