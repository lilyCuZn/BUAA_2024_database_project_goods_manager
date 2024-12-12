module.exports = {
  devServer: {
    host: "0.0.0.0",
    port: 8080,
    proxy: {
      "/web": {
        target: "http://10.193.115.252:8000",
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
