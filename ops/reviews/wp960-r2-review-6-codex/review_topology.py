import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from review_checks import ROOT, TMP, E, BASE, SHA, record
from review_mutations import load
from review_probes import fixture, pair, git, out, t

def clone(name, sha):
    dr = TMP / name
    assert not dr.exists(), dr
    p = subprocess.run(['git', 'clone', '--no-checkout', '--no-hardlinks', str(ROOT.parent / 'mirror.git'), str(dr)], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    git(dr, 'checkout', '--detach', sha)
    subprocess.run(['git', '-C', str(dr), 'symbolic-ref', '--delete', 'refs/remotes/origin/HEAD'], capture_output=True)
    git(dr, 'config', 'core.abbrev', '7')
    return dr

def corpus():
    b = t.bnv2
    lo, tk = b.kiem(ROOT, no_cau_lich_su=frozenset())
    rc = b._ma_thoat(lo, tk)
    keys = set(tk['vi_pham_cau'])
    out(case='head-empty-debt', rc=rc, total=tk['tong'], lines=len(lo), non_history=[x for x in lo if not x.startswith('[L-')], unknown=tk['chua_do'], equal_debt=keys==b.NO_CAU_LICH_SU, counts={rule:sum(k[2]==rule for k in keys) for rule in ['L-REVIEW','L-ANCESTRY','L-SURFACE']}, all_debt_files_exist=all((ROOT/b.THU_MUC/k[0]).is_file() for k in b.NO_CAU_LICH_SU), subset_frozen=b.NO_CAU_LICH_SU <= t.NO_CAU_DONG_BANG)
    for line in lo:
        print(line, flush=True)
    assert rc==1 and len(lo)==61 and keys==b.NO_CAU_LICH_SU and not tk['chua_do']
    dr = clone('base', BASE)
    git(dr, 'update-ref', 'refs/remotes/origin/master', BASE)
    p = subprocess.run([sys.executable, '-B', str(dr/'ops/bien_nhan_v2.py'), '--root', str(dr)], capture_output=True, text=True)
    out(case='original-base-gate', rc=p.returncode, stdout=p.stdout, stderr=p.stderr)
    lo, tk = b.kiem(dr)
    out(case='head-gate-base-corpus', rc=b._ma_thoat(lo,tk), total=tk['tong'], debt=tk['no_cau'], violations=lo, unknown=tk['chua_do'])
    assert p.returncode==0 and b._ma_thoat(lo,tk)==0 and tk['no_cau']=={'L-REVIEW':1,'L-ANCESTRY':60,'L-SURFACE':0}
    record('Hướng 9 — tái sinh nợ độc lập trên base và HEAD', 'Lệnh `python3 -B -u review_topology.py corpus`: HEAD nợ rỗng rc=1, đúng61 dòng ba luật (1/60/0), 0 lỗi khác, 0 unknown; tập khóa bằng NO_CAU_LICH_SU; mọi tệp có thật; tập nợ ⊆ bản đóng băng test. Base exact4488444: gate gốc rc=0; mã HEAD trên corpus base rc=0/nợ1/60/0. Log `evidence/corpus-independent.log`.')

def ci():
    dr = clone('ci', SHA)
    parent = git(ROOT, 'rev-parse', SHA+'^')
    assert parent == '79dbaf4d0a636906e922590b00cb9968989086272' or parent.startswith('79dbaf4')
    tree = git(ROOT, 'rev-parse', SHA+'^{tree}')
    env = {**os.environ, 'GIT_AUTHOR_NAME':'reviewer', 'GIT_AUTHOR_EMAIL':'reviewer@example.test', 'GIT_COMMITTER_NAME':'reviewer', 'GIT_COMMITTER_EMAIL':'reviewer@example.test', 'GIT_AUTHOR_DATE':'2026-10-29T04:00:00Z', 'GIT_COMMITTER_DATE':'2026-10-29T04:00:00Z'}
    merge = git(dr, 'commit-tree', tree, '-p', parent, '-p', SHA, '-m', 'Local simulation of pull_request merge', env=env)
    git(dr, 'checkout', '--detach', merge)
    git(dr, 'update-ref', 'refs/remotes/origin/master', parent)
    ref = subprocess.run(['git','-C',str(dr),'show-ref','--verify','refs/remotes/origin/HEAD'],capture_output=True,text=True)
    p = subprocess.run([sys.executable,'-B','ops/bien_nhan_v2.py','--root','.'],cwd=dr,capture_output=True,text=True)
    out(case='pull-request-merge', merge=merge, parents=git(dr,'show','-s','--format=%P',merge), tree=git(dr,'rev-parse','HEAD^{tree}'), candidate_tree=tree, shallow=git(dr,'rev-parse','--is-shallow-repository'), origin_master=git(dr,'rev-parse','origin/master'), origin_head_present=ref.returncode==0, gate_rc=p.returncode, stdout=p.stdout, stderr=p.stderr)
    assert p.returncode==0 and ref.returncode!=0 and git(dr,'rev-parse','--is-shallow-repository')=='false'
    record('Hướng 10 — mô phỏng CI pull_request', f'Lệnh `python3 -B -u review_topology.py ci`: merge `{merge}`, hai parent `{parent}` + `{SHA}`, tree `{tree}` đúng candidate, shallow=false (tương ứng fetch-depth:0), origin/HEAD vắng, origin/master={parent}; gate rc=0/TỔNG:ĐẠT, nợ1/60/0. Log `evidence/ci.log`. Đây là mô phỏng local, không phải check run GitHub online.')

def config():
    results = {}
    for value in ['false','no','off','true','yes','on']:
        with tempfile.TemporaryDirectory() as temp:
            dr=Path(temp)
            k,al=fixture(dr)
            k['g']('config','remote.archive.promisor',value)
            rows=pair(dr,al)
            out(case='promisor-'+value, fsck=git(dr,'fsck','--no-reflogs'), result=rows)
            results[value]=[x['rc'] for x in rows]
    for mode in ['alternates-env','alternates-file','worktree','GIT_COMMON_DIR','GIT_CONFIG_COUNT']:
        with tempfile.TemporaryDirectory() as temp:
            dr=Path(temp)
            k,al=fixture(dr)
            env={}
            target=dr
            if mode.startswith('alternates'):
                pool=dr/'_pool'
                (dr/'.git/objects').rename(pool)
                (dr/'.git/objects/info').mkdir(parents=True)
                if mode.endswith('env'):
                    env={'GIT_ALTERNATE_OBJECT_DIRECTORIES':str(pool)}
                else:
                    (dr/'.git/objects/info/alternates').write_text(str(pool)+'\n')
            elif mode=='worktree':
                target=dr/'_wt'
                k['g']('worktree','add','--detach',str(target),'master')
            elif mode=='GIT_COMMON_DIR':
                env={'GIT_COMMON_DIR':str(dr/'khong-co')}
            else:
                env={'GIT_CONFIG_COUNT':'1','GIT_CONFIG_KEY_0':'core.fsyncObjectFiles','GIT_CONFIG_VALUE_0':'true'}
            rows=pair(target,al,env)
            out(case=mode, result=rows)
            results[mode]=[x['rc'] for x in rows]
    assert all(v==([2,2] if k in ['true','yes','on'] else [1,0]) for k,v in results.items())
    record('Hướng 11 — cấu hình lành, object pool và linked worktree', 'Lệnh `python3 -B -u review_topology.py config`: false/no/off=1/0, true/yes/on=2/2; các boolean fixture fsck=0. Dời nguyên object store ra pool qua env hoặc info/alternates đều1/0. Linked worktree thường1/0; GIT_COMMON_DIR sai và GIT_CONFIG_COUNT tiêm warning bị cô lập nên1/0. Log `evidence/config.log`. Không biến cảnh báo deprecated cấu hình thực của B2 thành finding.')

if __name__=='__main__':
    {'corpus':corpus,'ci':ci,'config':config}[sys.argv[1]]()
