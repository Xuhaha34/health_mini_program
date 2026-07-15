// src/utils/export.js - Excel导出工具
import * as XLSX from 'xlsx'

export const exportToExcel = (data, filename = '导出数据', sheetName = 'Sheet1') => {
    
    const wb = XLSX.utils.book_new()
    
  
    const ws = XLSX.utils.json_to_sheet(data)
    
   
    XLSX.utils.book_append_sheet(wb, ws, sheetName)
    

    XLSX.writeFile(wb, `${filename}.xlsx`)
}


export const exportMultiSheet = (sheets, filename = '导出数据') => {
    const wb = XLSX.utils.book_new()
    
    Object.keys(sheets).forEach(sheetName => {
        const ws = XLSX.utils.json_to_sheet(sheets[sheetName])
        XLSX.utils.book_append_sheet(wb, ws, sheetName)
    })
    
    XLSX.writeFile(wb, `${filename}.xlsx`)
}
