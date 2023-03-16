# Configuration Manager

- should optionaly use repo pattern
- should save configs as different types

## ConfigManager:

The `ConfigManager` is a simple configuration manager that loads a single configuration at a time.

```
merge_strategy: None
merge_sections: []
writable: False
```

## HierarchyConfigManager:

The `HierarchyConfigManager` is a configuration manager that can be used to manager configurations. It is intended for system using Hierarchical File System (HFS).

```
enable_system_paths: False
enable_user_paths: False
enable_local_paths: True
```

## TreeConfigManager:

The `TreeConfigManager` is a configuration manager for configurations nested within structured directory layout. This can be conceptualized as Maven like nested-pom configurations
