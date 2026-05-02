import re


def clean_salary(raw: str) -> dict:
    """Normalize salary string into structured fields.

    Returns dict with: raw, min, max, type (月薪/日薪/面议), periods (e.g. 15 for 15薪)
    """
    result = {'raw': raw, 'min': None, 'max': None, 'type': '', 'periods': None}
    if not raw or raw == '面议':
        result['type'] = '面议'
        return result

    raw = raw.strip().replace(' ', '')

    if '面议' in raw:
        result['type'] = '面议'
        return result

    # 日薪: 300-500/天
    if '天' in raw or '日' in raw:
        result['type'] = '日薪'
        nums = re.findall(r'(\d+\.?\d*)', raw)
        if len(nums) >= 2:
            result['min'] = float(nums[0])
            result['max'] = float(nums[1])
        return result

    # 时薪: 20-30/时
    if '时' in raw:
        result['type'] = '时薪'
        nums = re.findall(r'(\d+\.?\d*)', raw)
        if len(nums) >= 2:
            result['min'] = float(nums[0])
            result['max'] = float(nums[1])
        return result

    result['type'] = '月薪'

    # Extract 薪 periods: 15薪, 16薪
    period_match = re.search(r'(\d+)\s*薪', raw)
    if period_match:
        result['periods'] = int(period_match.group(1))

    # Normalize: 15k-25k, 15K-25K, 15000-25000
    raw_lower = raw.lower()
    nums = re.findall(r'(\d+\.?\d*)', raw_lower)
    if len(nums) >= 2:
        m1, m2 = float(nums[0]), float(nums[1])
        # If values look like "15" → 15k, convert to thousands
        if 'k' in raw_lower:
            result['min'] = m1
            result['max'] = m2
        elif m1 < 100:  # Already k-notation without 'k'
            result['min'] = m1
            result['max'] = m2
        elif m1 >= 100:
            result['min'] = m1
            result['max'] = m2
    elif len(nums) == 1:
        result['min'] = float(nums[0])

    return result


def clean_experience(raw: str) -> str:
    """Normalize experience requirement to standard categories."""
    if not raw:
        return ''
    raw = raw.strip()
    if '不限' in raw or '经验不限' in raw:
        return '经验不限'
    if '应届' in raw or '在校' in raw:
        return '应届生'
    if '1年以下' in raw:
        return '1年以下'
    m = re.search(r'(\d+)-(\d+)年', raw)
    if m:
        return f'{m.group(1)}-{m.group(2)}年'
    m = re.search(r'(\d+)年以上', raw)
    if m:
        return f'{m.group(1)}年以上'
    return raw


def clean_education(raw: str) -> str:
    """Normalize education requirement to standard categories."""
    if not raw:
        return ''
    raw = raw.strip()
    mapping = {
        '初中及以下': '初中及以下', '高中': '高中',
        '大专': '大专', '本科': '本科',
        '硕士': '硕士', '博士': '博士',
        '学历不限': '学历不限',
    }
    for key, val in mapping.items():
        if key in raw:
            return val
    return raw


def clean_location(raw: str) -> dict:
    """Split location string into province/city/district."""
    result = {'province': '', 'city': '', 'district': ''}
    if not raw:
        return result

    raw = raw.strip()
    # City-level municipalities: 北京, 上海, 天津, 重庆
    municipalities = {'北京': '北京', '上海': '上海', '天津': '天津', '重庆': '重庆'}

    # Simple heuristic: first 2-3 chars = city
    for mun in municipalities:
        if raw.startswith(mun):
            result['province'] = mun
            result['city'] = mun
            rest = raw[len(mun):]
            if rest.endswith('区') or rest.endswith('县'):
                result['district'] = rest
            break
    else:
        # Province-level: e.g. 广东省深圳市南山区
        if '省' in raw:
            prov_end = raw.index('省')
            result['province'] = raw[:prov_end + 1]
            raw = raw[prov_end + 1:]
        # City
        if '市' in raw:
            city_end = raw.index('市')
            result['city'] = raw[:city_end + 1]
            raw = raw[city_end + 1:]
        elif raw and not result['city']:
            result['city'] = raw[:min(3, len(raw))]
        # District
        if raw and (raw.endswith('区') or raw.endswith('县') or raw.endswith('街道')):
            result['district'] = raw

    return result
