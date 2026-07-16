#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恶意文件哈希数据库
Malicious File Hashes Database - 银狐木马 IOC
"""

class MaliciousHashes:
    """恶意文件哈希"""
    
    def __init__(self):
        # 银狐病毒已知的恶意文件哈希
        self.hashes = [
            # ========== 2026年7月 - ValleyRAT八阶段攻击 ==========
            # trojanized installer
            "520304a1cabdd9aa05c0a769c3874bc3cc2608d8e71ae607ca2bdf96b298b5de",
            # malicious email
            "e8be03f19ada1f5cec74b143e21d4939e781671d",
            # ZIP archives
            "65168c8dd93b16d3b77092fb70c0fa6fba4dffcc",
            "eca7ed7b699835fadc2c2997a2845864e02b8dfe",
            
            # ========== 2026年7月 - 伪装Steam/Telegram ==========
            "D58F9D3409892188764DA6F311E915FD",
            "E0F6227F02D8BF6263938088AF91D3F073DB4A43A529BA46665CB2E90F612799",
            
            # ========== 2026年6月 - WDAC策略攻击 ==========
            # (无特定哈希，使用行为检测)
            
            # ========== 2026年5月 - CNCERT通报 ==========
            # (批量钓鱼站点，无特定哈希)
            
            # ========== 2026年3月 - 自编写驱动+Unhooking ==========
            "fd6b3cd8fd14f7d589ed68deeb07d425c907ed828be8006c3f1962cf365f6cd7",
            
            # ========== 2026年2-4月 - 税务主题ABCDoor ==========
            "e6362a81991323e198a463a8ce255533",
            "2c5a1dd4cb53287fe0ed14e0b7b7b1b7",
            "5b998a5bc5ad1c550564294034d4a62c",
            "c50c980d3f4b7ed970f083b0d37a6a6a",
            "de8f0008b15f2404f721f76fac34456a",
            "9bf9f635019494c4b70fb0a7c0fb53e4",
            "a543b96b0938de798dd4f683dd92a94a",
            "fa08b243f12e31940b8b4b82d3498804",
            "13669b8f2bd0af53a3fe9ac0490499e5",
            "055c3fff8f1f58a41e7571b9bd7ebf4b1b10ba5231f1ffbcb47e0307d7ff6072",
            "06ecf34ecf1f3f56a1760b8757b978d6bd859adcf699af4adfbeb0982e41282a",
            "8cb036bcc7aacf7393575ddf15133e24d3a22cc92a4b14e8595686e4bf806256",
            "e2b75baeb7ed21fb8f27984f941286770d1c3c0b60fce8d7fa5b167bd24ba6dc",
            
            # ========== 2026年1月 - 伪装Telegram ==========
            "dd9c53633660213eb7d8cca3c2add9bb",
            "6d0129128c6ee34a66a56afbb2a45bc7",
            "47447c032b04bd8dcf566e4526",
            "a0fd0e9190330729f5896b3900d2250b",
            "12400581583a1faef1fbcf223775939cc468a1a27ea346261278cb14cfe40a15",
            "31f731866d1e6244bfc64daab4f89491",
            "4eaedd9bc5de9c64b8a173c9093f7fa3d4d82e863f347d51314c8b8042cbbf40",
            
            # ========== 2025年12月-2026年1月 - 网易CC借壳 ==========
            "3b94a5d1342d68a316cb696597ceb3be02103d3c94b763bc688aacfc3d3f14f5",
            "d59b88ad84ba8853f423ebdd59afd656c27a7be9dd1e4825c6f85587b82f1005",
            "6A46E4C5DE23FD904EF19130526016C7B38586F9BA136CF2B8318D1F41BB30D6",
            "2b68aaf3d7428d1f0bd9345372d547b065d5fabeba0c1bdb9e48045cf43d5ffd",
            "6b4bbbce480fbc50d39a8ec4b72cdb7d781b151921e063dd899fd9b736adcf68",
            
            # ========== 2026年1月 - 伪装Chrome ==========
            "8c53aab5d025a82ad83705f4f0c9071a1e5810fe",
            
            # ========== 2025年12月-2026年1月 - 伪装搜狗输入法 ==========
            "89dc8df1ace5d385c07f437c03431d33",
            "33a9619d2dce9cd7298a78dd21293775",
            "2FAB10855EFC0DC62A255FF1E6EC8FA6",
            "1D1464C73252978A58AC925ECE57F0FB",
            
            # ========== 2024年10月 - 银狐IOC清单 ==========
            "6F88E1D533F0812A63AFEE747FA34B65142918B61F5189C03180E3CC01D41A4A",
            "68B06C910D589B9CE464E5FDC29215321EDE727F196469D17901ACCE43F554C2",
            "26C84ACCFB461A7AA3EF567DE5FCF723F5BA6283F9C9FEFE60B42498B638FBFD",
            "AAC33F3C3A2E2E0640EBA8858376403E2D561AB44D0DA395F5347F483CA1B001",
            "7FEE7909A7C3366BC7DC071484B37A124E04B39784C482BFD1793A15F6D8682C",
            "8ABA58D8097504A55985BEDC03101194C0529523F4235D893B7DD7F2F1A9DFAE",
            "2be5917a043662ade1f5dcfd594ab6135a040d23480c43a3f9d525d093d08c2b",
            "11d3b43e293e794d53ca136e09c518379641bbfe39698f53d1262c87eaf63d6d",
            "db05ebc2ef9f4c71d1a11eda48d2b53e73ebf7348b324862d1aec198a90cbc2e",
            "d3cb37a362418b800bcb47079047a5c370662965ee0a2ba576a40236b21b0acf",
            "4a6805b8ebe75010419b1320b1b8da84f9ea7647d124c965bd83d6eae0f62328",
            "5d6194270f505b49f7b1289249605bf7000b97f52aa9f06cb7c1e94c50d71d39",
            "6d6ba2bc9ad414837826f7278bc3e0116f1aeda02d0c2284ed65819f5d9180a8",
            "dd1e2826c0124a6d4f7397a5a71f633928926c0608b62fb9e615ba778acc39ff",
            "512a3141098f324fa7d908fe571e6af4abcaa5b7f3f7b6cd8970100985080769",
            "089626adeaca613daf9daa1c8daf7633bcab34cafaa4ce3df9d12a3bbe595531",
            "c349a830fbeae9cf7dbb9470a84662970734c17c7d818ce5be553e5046e5c7bb",
            
            # ========== 2026年3月 - 瑞安研分析 ==========
            "a7471e097d4d4e84fa44a025603499e1",
            
            # ========== 2026年1月 - "违纪名单" ==========
            "c5744d2c8697a5c8f0f17027b7be393157c871498e03b1d266598778692239d5",
            
            # ========== 2024年变种 ==========
            "34101194d27df8bc823e339d590e18f2",
            "cf8088b59ee684cbd7d43edcc42b2eec",
            "f3cad147e35f236772b5e10f4292ba6e",
            "0dadf900cfb946cf2abec3a65d288acd",
            "a3b107395ee1ecee13674554cb410791",
            "b09a5b62152b21e1cdd4517d0c49f516",
            "260521432d424ac3aa826de748e987cb",
            "833a7c8344df149859f00277ac5b2751",
            "503d2e8bcbe83c475273c965a64efe02",
            "1654ac65b2d728575078b413fe5d41df",
            "750cac46994e82ba83ff142dd6ee2e3d",
            "c5109d20dc5ca3b1bf5ab5175389d0d1",
            "3cbd704a35789431be7a19ebfcff7dc2",
            "a68f7de26252cf4d7f6d6c6259c58741",
            "dc964ea4e2725332ee70d394d7237946",
            "64215587dc6863b9b0a71bb95dba1164",
            "0be9fc43bb6581574a1e46884f8e7688",
            "b81e57f53615405fe30c58af27c22b52",
            "026a5407ac53ac6ef68f5de78ffb3ae3",
            "84dcef26e3284b0bb5c9cb3fd405b140",
            "1215cb125ea2d2d00c3e839fb56af787",
            "48ab5ef59884e263651d874dcff59ab0",
            "09ffdc1f4d2a3d9115d79f82b9024e9a",
            "3eb270f628533a2a9e8afadcdfb418f2",
            "ec373011704e5baf4821273cb373e419",
            "747959625308d11e1530d87aeab54af3",
            "4e0f706c773796ec4daa2e487cd66f9f",
            "205f9668ce6a52dc1e8a95201097d766",
            "af811acb947b4299d68dd792e9fe0625",
            "7f98842b6d79cdd00930e949d5ad95a5",
            "995010298fb1d25d492112e12d9a06a0",
            "d863cc94fe006cce2eb130dbc14a3e74",
            "12532d6f8434b4f1e6b1ec7b98ef8e91",
            "887a04cda34f7af3f350fd5f4d7a10c2",
            "21a41eea0c4a12ac80a0a41dd06b86c6",
            "c17aa0a7bc88d9f753fdd5cb13be697a",
            "ed7d98ec86252ba3f73d92f7d08513ea",
            "e90bafa40809c64f1535bf1684b14ee4",
            "9c6b3ebb6719f90e638aa097825e5bd3",
            "2f202856508ad743315739b0b8164e45",
            "edc41e28dc9c16705b6658f8536c8101",
            "bb5c8121a1748a170d4cc5e16f40093e",
            "93a8cc0f7a074b83e34f6e89c538005c",
            "4479178d28e07bd1eef068ef15a83d47",
            "5361f396d10252751b39c06af8168c34",
            "277034be6ced435eee05828efc667a7c",
            "f0cdb673d986220b1acb66b965430be7",
            "254943ea6620a11127ee127ba8d3d447",
            "a1ed0088746b3c32069f9c03b29941c3",
            "122113733ebd64e52e574cbfe2488f04",
            "4dbf6b59106684ac56d63448d7af432c",
            "530781bfc00af3cb514224c395fb8cc9",
            "bf198e28de8258f0e245e39eb3f21ab7",
            "59b52b546ec7c5eb47b774dde279b904",
            "f669cd352cb4b4d1162524a17f5dc768",
            "adfbd1410f57f6bdc91aa4c9b4cd7c51",
            "a63228536a7c5265c9bace82cd40420c",
            "91128221df26497fc8b7534c6fa90dcc",
            "5725f3c1bc663b7d780ad76fe0cf865f",
            "cfe4b550cf32fea3d910b8ed6763435a",
            "57d47b4c6065361eaf3ae0efbb4d59f4",
            "a7471e097d4d4e84fa44a025603499e1",
            "33a9619d2dce9cd7298a78dd21293775",
            "2FAB10855EFC0DC62A255FF1E6EC8FA6",
            "1D1464C73252978A58AC925ECE57F0FB",
            "32407207e9e9a0948d167dca96c41d1a",
            "d17caf6f5d6ba3393a3a865d1c43c3d2",
        ]
        valid_lengths = {32, 40, 64}
        self.hashes = list(dict.fromkeys(
            value.lower() for value in self.hashes
            if len(value) in valid_lengths and all(char in '0123456789abcdefABCDEF' for char in value)
        ))
    
    def get_hashes(self):
        """获取所有恶意文件哈希"""
        return self.hashes
    
    def add_hash(self, file_hash):
        """添加新的恶意文件哈希"""
        if file_hash not in self.hashes:
            self.hashes.append(file_hash)
    
    def remove_hash(self, file_hash):
        """移除恶意文件哈希"""
        if file_hash in self.hashes:
            self.hashes.remove(file_hash)
    
    def is_malicious(self, file_hash):
        """检查文件哈希是否是恶意的"""
        return file_hash.lower() in self.hashes
    
    def get_hash_count(self):
        """获取恶意文件哈希数量"""
        return len(self.hashes)
    
    def search_hash(self, query):
        """搜索哈希（支持部分匹配）"""
        query_lower = query.lower()
        return [h for h in self.hashes if query_lower in h.lower()]
