# wht-md5 轻量级加密插件

🎉 首次发布！一个轻量、快速、跨平台的MD5加密工具，完美支持Vue2/Vue3

## 🌟 特性
- 💪 纯JavaScript实现，零依赖
- ⚡️ 高性能，支持多次加密
- 🔄 灵活的大小写输出
- 📱 多端完美适配
- 🎯 支持16位/32位输出
- ⚛️ 支持Vue2/Vue3

## 🛠 兼容性
| 平台 | 支持情况 |
|------|---------|
| Vue2 | ✅ 已支持 |
| Vue3 | ✅ 已支持 |
| H5   | ✅ 已支持 |
| 微信小程序 | ✅ 已支持 |
| App  | ✅ 已支持 |
| 其他小程序 | 理论支持，需自测 |

## 📦 安装
uni_modules 插件市场搜索 `wht-md5` 安装即可

## 🚀 快速开始

### Vue2
```vue
<script>
import whtMd5 from '@/uni_modules/wht-md5/js_sdk/wht-md5.js'

export default {
    methods: {
        encrypt() {
            // 32位加密（默认）
            const hash32 = whtMd5('hello')  // 5d41402abc4b2a76b9719d911017c592
            
            // 16位加密
            const hash16 = whtMd5('hello', { length: 16 })  // 5d41402abc4b2a76
            
            // 大写输出
            const hashUpper = whtMd5('hello', { uppercase: true })  // 5D41402ABC4B2A76B9719D911017C592
            
            // 多次加密
            const hashMulti = whtMd5('hello', { iterations: 3 })
        }
    }
}
</script>
```

### Vue3
```vue
<script setup>
import whtMd5 from '@/uni_modules/wht-md5/js_sdk/wht-md5.js'

const encrypt = () => {
    // 32位加密（默认）
    const hash32 = whtMd5('hello')  // 5d41402abc4b2a76b9719d911017c592
    
    // 16位加密
    const hash16 = whtMd5('hello', { length: 16 })  // 5d41402abc4b2a76
    
    // 大写输出
    const hashUpper = whtMd5('hello', { uppercase: true })  // 5D41402ABC4B2A76B9719D911017C592
    
    // 多次加密
    const hashMulti = whtMd5('hello', { iterations: 3 })
}
</script>
```

## 💡 高级用法
```javascript
// 组合使用多个选项
const hash1 = whtMd5('hello', { 
    uppercase: true,  // 大写输出
    length: 16,      // 16位长度
    iterations: 2    // 加密2次
})

// 创建预设配置
const md5WithOptions = whtMd5.withOptions({
    uppercase: true,
    length: 16,
    iterations: 2
})

// 使用预设配置
const hash2 = md5WithOptions('hello')
const hash3 = md5WithOptions('world')
```

## 📖 API文档

### 基础方法
```javascript
whtMd5(string, options?)
```

### 配置选项
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| uppercase | Boolean | false | 是否输出大写结果 |
| iterations | Number | 1 | 加密次数，范围1-10 |
| length | Number | 32 | 输出长度，可选16或32 |

### withOptions 工具方法
```javascript
// 创建预设配置的加密函数
const md5WithOptions = whtMd5.withOptions(options)
```

## ⚠️ 注意事项
1. 加密次数限制在1-10次，超过会自动限制为10
2. 输出长度只支持16位和32位，默认32位
3. 大量数据加密建议使用 Web Worker

## 🔄 版本记录
查看 [更新日志](./changelog.md)

## 📝 协议
MIT License

## 🤝 贡献
欢迎提交 issue 和 PR