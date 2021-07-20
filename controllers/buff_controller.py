from models.Buff import Buff


def get_effects_str(buff: Buff, associated_value=None) -> list[str]:
    detailed_effects = []
    count = 0
    for effect in buff.effects:
        corrected_effect = effect
        if associated_value is not None:
            corrected_effect = corrected_effect.replace('/v', associated_value)
        if count >= len(buff.key_effect_data):
            detailed_effects.append(corrected_effect)
        else:
            detailed_effects.append(corrected_effect.replace('/$', str(buff.key_effect_data[count])))
        count += 1
    return detailed_effects
