def get_usage_data(config_file, section, attribute):
    return config_file.get(section, attribute)


def section_exists(config_file, section):
    return config_file.has_section(section)