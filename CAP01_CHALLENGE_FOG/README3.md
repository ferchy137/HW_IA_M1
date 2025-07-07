````mermaid
graph TD
    A[Start] --> B{Input: numbers (list)};
    B --> C{n = len(numbers)};
    C --> D{i = 0};
    D --> E{i < n?};
    E -- Yes --> F{j = 0};
    F --> G{j < n - i - 1?};
    G -- Yes --> H{numbers[j] > numbers[j + 1]?};
    H -- Yes --> I{Swap numbers[j] and numbers[j + 1]};
    I --> J{j = j + 1};
    J --> G;
    G -- No --> K{i = i + 1};
    K --> E;
    E -- No --> L{Return numbers};
    L --> M[End];
    ````