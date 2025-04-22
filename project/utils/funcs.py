from collections import defaultdict, deque


def compute_critical_path(tasks_list):
    tasks = {t.id: t for t in tasks_list}
    graph = defaultdict(list)
    in_deg = defaultdict(int)
    out_deg = defaultdict(int)

    # Build graph
    for t in tasks_list:
        for d in t.dependencies:
            graph[d.id].append(t.id)
            in_deg[t.id] += 1
            out_deg[d.id] += 1

    # Topological sort with level tracking
    queue = deque((tid, 0) for tid in tasks if in_deg[tid] == 0)
    top_order, levels = [], defaultdict(list)

    while queue:
        tid, lvl = queue.popleft()
        top_order.append(tid)
        levels[lvl].append(tid)
        for neighbor in graph[tid]:
            in_deg[neighbor] -= 1
            if in_deg[neighbor] == 0:
                queue.append((neighbor, lvl + 1))

    # Longest path calculation
    dist = {tid: tasks[tid].days_to_complete for tid in tasks}
    prev = {tid: None for tid in tasks}

    for tid in top_order:
        for neighbor in graph[tid]:
            new_dist = dist[tid] + tasks[neighbor].days_to_complete
            if new_dist > dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = tid

    # Get critical path
    leaves = [tid for tid in tasks if out_deg[tid] == 0]
    end = max(leaves, key=lambda tid: dist[tid])

    path = []
    while end:
        path.insert(0, end)
        end = prev[end]

    return path, levels, dist[path[-1]]

