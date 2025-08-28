["id", "created_at", "name", "has_test", "alternate_url"] as $headers |
$headers,
(.items[] | 
    select(type == "object") |
    [
        .id,
        .created_at,
        .name,
        (.has_test // false),  
        .alternate_url
    ]
) |
@csv