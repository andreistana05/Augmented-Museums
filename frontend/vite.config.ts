import basicSsl from "@vitejs/plugin-basic-ssl";

export default {
  plugins: [basicSsl()],
  server: {
    host: true,
    proxy: { "/api": "http://localhost:8000" },
  },
};