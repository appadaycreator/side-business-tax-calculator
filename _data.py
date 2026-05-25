TITLE = '副業税金計算ツール【無料】2024年確定申告・住民税対策'
DESCRIPTION = '副業収入から所得税・住民税の概算を計算。確定申告が必要な年収ラインや節税ポイントをわかりやすく解説します。'
DESCRIPTION_SHORT = '副業収入・本業年収から所得税・住民税の概算と確定申告の要否を計算...'
COLOR1 = '#FFFBEB'
COLOR2 = '#FEF3C7'
COLOR_BTN = '#D97706'
FOOTER_LINKS = [('https://appadaycreator.com/blog-income-advisor/', 'ブログ収益化診断'), ('https://appadaycreator.com/freelance-rate-calculator/', 'フリーランス単価計算'), ('https://appadaycreator.com/household-budget-analyzer/', '家計簿診断ツール')]

CUSTOM_CSS = ""

MAIN_HTML = """<div class="card">
  <h2 style="font-size:18px;font-weight:700;margin-bottom:12px;">💰 副業税金計算ツール（2024年版）</h2>
  <p style="color:#666;font-size:14px;margin-bottom:16px;">副業収入と本業年収を入力して税負担の概算を計算します</p>
  <label>本業の年収（給与）</label>
  <div style="display:flex;align-items:center;gap:8px;margin-top:4px;">
    <input type="number" id="main-income" placeholder="例: 5000000" min="0" step="100000" style="flex:1;">
    <span style="font-size:14px;color:#666;">円</span>
  </div>
  <label>副業の年間収入（売上・報酬総額）</label>
  <div style="display:flex;align-items:center;gap:8px;margin-top:4px;">
    <input type="number" id="side-income" placeholder="例: 300000" min="0" step="10000" style="flex:1;">
    <span style="font-size:14px;color:#666;">円</span>
  </div>
  <label>副業の年間経費（見込み）</label>
  <div style="display:flex;align-items:center;gap:8px;margin-top:4px;">
    <input type="number" id="expenses" placeholder="例: 50000（経費ゼロなら0）" min="0" step="10000" style="flex:1;">
    <span style="font-size:14px;color:#666;">円</span>
  </div>
  <label>副業の種類</label>
  <select id="type">
    <option value="misc">雑所得（ライティング・YouTube・ハンドメイド等）</option>
    <option value="biz">事業所得（フリーランス・コンサル・個人事業）</option>
    <option value="real">不動産所得（家賃収入）</option>
  </select>
  <button class="btn" style="margin-top:20px;" onclick="calc()">計算する →</button>
</div>
<div class="result" id="result">
  <div class="card">
    <h3 style="font-size:16px;font-weight:700;color:#D97706;margin-bottom:12px;">📊 税金概算シミュレーション</h3>
    <div id="r-detail" style="font-size:14px;line-height:2.2;"></div>
    <div id="r-alert" style="margin-top:12px;border-radius:10px;padding:14px;font-size:13px;line-height:1.8;"></div>
    <div style="background:#FFFBEB;border-radius:10px;padding:12px;margin-top:12px;font-size:12px;color:#777;">
      ※本ツールの計算は概算です。正確な税額は税理士または所轄の税務署にご確認ください。
    </div>
    <button class="btn" style="margin-top:16px;" onclick="location.reload()">もう一度計算</button>
  </div>
</div>"""

JS_CODE = """function calcTax(income) {{
  const brackets = [[1950000,0.05,0],[3300000,0.10,97500],[6950000,0.20,427500],[9000000,0.23,636000],[18000000,0.33,1536000],[40000000,0.40,2796000],[Infinity,0.45,4796000]];
  for(const [limit,rate,deduct] of brackets) {{
    if(income<=limit) return Math.floor(income*rate-deduct);
  }}
  return 0;
}}
function getSalaryDeduction(income) {{
  if(income<=1625000) return 550000;
  if(income<=1800000) return Math.floor(income*0.4)-100000;
  if(income<=3600000) return Math.floor(income*0.3)+80000;
  if(income<=6600000) return Math.floor(income*0.2)+440000;
  if(income<=8500000) return Math.floor(income*0.1)+1100000;
  return 1950000;
}}
function calc() {{
  const main=parseInt(document.getElementById('main-income').value)||0;
  const side=parseInt(document.getElementById('side-income').value)||0;
  const exp=parseInt(document.getElementById('expenses').value)||0;
  const type=document.getElementById('type').value;
  if(!main||!side){{alert('本業年収と副業収入を入力してください');return;}}
  const sideNet=Math.max(0,side-exp);
  const basicDeduct=480000;
  const mainDeduct=getSalaryDeduction(main);
  const mainTaxableBase=Math.max(0,main-mainDeduct-basicDeduct);
  const totalTaxable=mainTaxableBase+sideNet;
  const taxBefore=calcTax(mainTaxableBase);
  const taxAfter=calcTax(totalTaxable);
  const addedIncomeTax=Math.max(0,taxAfter-taxBefore);
  const residentTax=Math.floor(sideNet*0.10);
  const totalAdd=addedIncomeTax+residentTax;
  const detail=document.getElementById('r-detail');
  detail.innerHTML=`
    <div style="display:flex;justify-content:space-between;border-bottom:1px solid #f3e5b3;padding:4px 0;"><span>副業の純利益（収入−経費）</span><strong>${{sideNet.toLocaleString()}}円</strong></div>
    <div style="display:flex;justify-content:space-between;border-bottom:1px solid #f3e5b3;padding:4px 0;"><span>追加の所得税（概算）</span><strong>${{addedIncomeTax.toLocaleString()}}円</strong></div>
    <div style="display:flex;justify-content:space-between;border-bottom:1px solid #f3e5b3;padding:4px 0;"><span>追加の住民税（概算）</span><strong>${{residentTax.toLocaleString()}}円</strong></div>
    <div style="display:flex;justify-content:space-between;padding:4px 0;font-size:16px;"><span><strong>合計追加税負担</strong></span><strong style="color:#D97706;">${{totalAdd.toLocaleString()}}円</strong></div>
    <div style="display:flex;justify-content:space-between;padding:4px 0;color:#888;font-size:13px;"><span>手取り実収入（概算）</span><span>${{Math.max(0,sideNet-totalAdd).toLocaleString()}}円</span></div>
  `;
  let alert='';
  if(sideNet>200000) {{
    alert=`<div style="background:#FEF2F2;border-left:4px solid #EF4444;padding:12px;border-radius:0 8px 8px 0;">⚠️ <strong>確定申告が必要です</strong><br>給与所得者で副業の所得（収入−経費）が20万円を超えるため、確定申告が必要です（翌年2月16日〜3月15日）。青色申告（65万円控除）の活用で節税できます。</div>`;
  }} else if(sideNet>0) {{
    alert=`<div style="background:#F0FDF4;border-left:4px solid #16A34A;padding:12px;border-radius:0 8px 8px 0;">✅ <strong>確定申告は不要</strong>（条件付き）<br>給与所得者の場合、副業の所得が20万円以下なら確定申告不要（所得税のみ）。ただし住民税申告は別途必要な場合があります。</div>`;
  }}
  if(type==='biz') alert+=`<div style="margin-top:8px;background:#FFFBEB;border-left:4px solid #D97706;padding:12px;border-radius:0 8px 8px 0;">💡 事業所得なら<strong>青色申告特別控除（最大65万円）</strong>が使えます。freeeやマネーフォワードで帳簿をつけておきましょう。</div>`;
  document.getElementById('r-alert').innerHTML=alert;
  document.getElementById('result').classList.add('show');
  document.getElementById('result').scrollIntoView({{behavior:'smooth'}});
}}"""
