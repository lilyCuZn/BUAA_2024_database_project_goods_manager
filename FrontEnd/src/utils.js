import axios from "axios";
import * as XLSX from "xlsx";

export default {
  install(Vue) {
    Vue.prototype.$Backend = async function (request) {
      try {
        console.log("request:", request);
        const response = await axios.post(
          "/web/process_frontend/",
          request,
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log("Backend response:");
        console.log(response.data);
        return response.data;
      } catch (error) {
        console.error(error);
        return null;
      }
    };
    Vue.prototype.$getColumnWidths = function (data) {
      const columnWidths = [];

      data.forEach((row) => {
        Object.keys(row).forEach((key, index) => {
          const value = row[key];
          const valueLength = value
            ? String(value).length
            : 0;

          columnWidths[index] = Math.max(
            columnWidths[index] || 0,
            valueLength
          );
        });
      });

      return columnWidths.map((width) => ({
        wch: width + 10,
      }));
    };
    Vue.prototype.$ExportFile = function (data, fileName) {
      const ws = XLSX.utils.json_to_sheet(data);
      const columnWidths =
        Vue.prototype.$getColumnWidths(data);
      ws["!cols"] = columnWidths;
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
      const excelBuffer = XLSX.write(wb, {
        bookType: "xlsx",
        type: "array",
      });
      const blob = new Blob([excelBuffer], {
        type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = fileName;
      link.click();
      URL.revokeObjectURL(link.href);
    };
  },
};
