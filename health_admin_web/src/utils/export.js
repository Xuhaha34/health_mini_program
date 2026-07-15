// src/utils/export.js - Excel导出工具
import * as XLSX from 'xlsx'

/**
 * 导出数据为Excel文件
 * @param {Array} data - 数据数组
 * @param {String} filename - 文件名
 * @param {String} sheetName - 工作表名称
 */
export const exportToExcel = (data, filename = '导出数据', sheetName = 'Sheet1') => {
    // 创建工作簿
    const wb = XLSX.utils.book_new()
    
    // 创建工作表
    const ws = XLSX.utils.json_to_sheet(data)
    
    // 将工作表添加到工作簿
    XLSX.utils.book_append_sheet(wb, ws, sheetName)
    
    // 导出文件
    XLSX.writeFile(wb, `${filename}.xlsx`)
}

/**
 * 导出多工作表Excel
 * @param {Object} sheets - 多个工作表 { sheetName: data }
 * @param {String} filename - 文件名
 */
export const exportMultiSheet = (sheets, filename = '导出数据') => {
    const wb = XLSX.utils.book_new()
    
    Object.keys(sheets).forEach(sheetName => {
        const ws = XLSX.utils.json_to_sheet(sheets[sheetName])
        XLSX.utils.book_append_sheet(wb, ws, sheetName)
    })
    
    XLSX.writeFile(wb, `${filename}.xlsx`)
}
