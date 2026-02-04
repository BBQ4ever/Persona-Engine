import json
import random
import copy
from datetime import datetime

class GenomeRecombinator:
    """
    Phase 6: 基因杂交引擎 (Constrained Recombination)
    实现数字人格的“繁育”与特征遗传。
    """
    def __init__(self, mutation_rate=0.05):
        self.mutation_rate = mutation_rate
        # 定义不可更改的安全锚点位点（示例：逻辑准确度等）
        self.safety_anchors = ["truth_alignment", "logic_gate"]

    def recombine(self, parent_a: dict, parent_b: dict, child_id: str) -> dict:
        """
        将两个父本基因杂交生成子本。
        """
        child_loci = []
        
        # 建立位点字典方便查询
        loci_a = {l['id']: l for l in parent_a['loci']}
        loci_b = {l['id']: l for l in parent_b['loci']}
        
        # 获取所有唯一的位点 ID
        all_ids = set(loci_a.keys()) | set(loci_b.keys())
        
        for locus_id in all_ids:
            # 1. 简单交叉 (Crossover)
            if locus_id in loci_a and locus_id in loci_b:
                # 两个父本都有，随机选一个或混合
                parent_choice = random.choice([loci_a[locus_id], loci_b[locus_id]])
                locus = copy.deepcopy(parent_choice)
                
                # 如果是数值范围型，尝试进行均值混合（或加权混合）
                if locus['distribution']['type'] == 'range':
                    val_a = loci_a[locus_id]['distribution']['values']['default']
                    val_b = loci_b[locus_id]['distribution']['values']['default']
                    # 混合后的 default 值为双亲均值
                    locus['distribution']['values']['default'] = (val_a + val_b) / 2
            else:
                # 只有一个父本有，直接继承
                locus = copy.deepcopy(loci_a.get(locus_id) or loci_b.get(locus_id))

            # 2. 突变 (Mutation) - 除非是安全锚点
            if locus_id not in self.safety_anchors and random.random() < self.mutation_rate:
                locus = self._apply_mutation(locus)
                
            child_loci.append(locus)

        # 构造子本 Genome 结构
        child_genome = {
            "version": parent_a["version"],
            "metadata": {
                "persona_id": child_id,
                "author": "GenomeRecombinator",
                "parents": [parent_a["metadata"]["persona_id"], parent_b["metadata"]["persona_id"]],
                "created_at": datetime.utcnow().isoformat() + "Z"
            },
            "loci": child_loci
        }
        
        return child_genome

    def _apply_mutation(self, locus: dict) -> dict:
        """
        引入微小的突变偏移。
        """
        if locus['distribution']['type'] == 'range':
            vals = locus['distribution']['values']
            drift = (random.random() * 0.2 - 0.1) # [-0.1, 0.1]
            new_def = vals['default'] + drift
            # 保持在边界内
            vals['default'] = max(vals['min'], min(vals['max'], new_def))
            print(f"🧬 MUTATION: Locus '{locus['id']}' drifted by {drift:.3f}")
            
        return locus

if __name__ == "__main__":
    # 测试杂交
    with open("src/l2_genome/sample_genome.json", "r") as f:
        pa = json.load(f)
    with open("src/l2_genome/parent_b_genome.json", "r") as f:
        pb = json.load(f)
        
    engine = GenomeRecombinator(mutation_rate=0.3) # 调高突变率方便观察
    child = engine.recombine(pa, pb, "pioneer_jester_mix_v1")
    
    # 打印结果对比
    print("\n[GENOME RECOMBINATION RESULT]")
    for locus in child['loci']:
        print(f"- Locus: {locus['id']} | Category: {locus['category']}")
        if locus['distribution']['type'] == 'range':
            print(f"  Default Value: {locus['distribution']['values']['default']:.3f}")
    
    # 保存结果
    with open("src/l2_genome/child_genome.json", "w") as f:
        json.dump(child, f, indent=4)
    print("\n✅ Child genome saved to src/l2_genome/child_genome.json")
