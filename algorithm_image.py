import matplotlib.pyplot as plt

# Імітація вашого класу DiskScheduler для побудови графіків
class DiskScheduler:
    def __init__(self, tracks=500, current_track=0, rotation_delay=8):
        self.tracks = tracks
        self.current_track = current_track
        self.rotation_delay = rotation_delay

    def calculateSeekTime(self, track):
        seekDistance = abs(self.current_track - track)
        trackSeekTime = seekDistance * 10
        outerTrackSeekTime = 130
        totalSeekTime = trackSeekTime + (seekDistance * outerTrackSeekTime)
        return totalSeekTime + self.rotation_delay

    def fcfs(self, requestQueue):
        total_time = 0
        sequence = []
        for track in requestQueue:
            total_time += self.calculateSeekTime(track)
            self.current_track = track
            sequence.append(total_time)
        return sequence

    def sstf(self, requestQueue):
        total_time = 0
        sequence = []
        while requestQueue:
            next_track = min(requestQueue, key=lambda x: abs(self.current_track - x))
            total_time += self.calculateSeekTime(next_track)
            self.current_track = next_track
            sequence.append(total_time)
            requestQueue.remove(next_track)
        return sequence

    def look(self, requestQueue):
        total_time = 0
        sequence = []
        direction = 1
        while requestQueue:
            if direction == 1:
                available_tracks = [track for track in requestQueue if track > self.current_track]
                if not available_tracks:
                    direction = -1
                    continue
                next_track = min(available_tracks)
            else:
                available_tracks = [track for track in requestQueue if track < self.current_track]
                if not available_tracks:
                    direction = 1
                    continue
                next_track = max(available_tracks)

            total_time += self.calculateSeekTime(next_track)
            self.current_track = next_track
            sequence.append(total_time)
            requestQueue.remove(next_track)
        return sequence

    def lfu(self, requestQueue, numSegments=3):
        total_time = 0
        sequence = []
        # Проста імітація LFU
        segments = [requestQueue[i::numSegments] for i in range(numSegments)]
        for segment in segments:
            for track in sorted(segment):
                total_time += self.calculateSeekTime(track)
                self.current_track = track
                sequence.append(total_time)
        return sequence

# Тестова черга запитів
test_request_queue = [143, 86, 147, 91, 171, 19, 62, 96, 78, 9, 10]

# Створення екземпляра DiskScheduler
scheduler = DiskScheduler()

# Отримання послідовностей для кожного алгоритму
fcfs_sequence = scheduler.fcfs(test_request_queue.copy())
sstf_sequence = scheduler.sstf(test_request_queue.copy())
look_sequence = scheduler.look(test_request_queue.copy())
lfu_sequence = scheduler.lfu(test_request_queue.copy())

# Побудова графіків
plt.figure(figsize=(12, 8))
plt.plot(fcfs_sequence, label='FCFS', marker='o')
plt.plot(sstf_sequence, label='SSTF', marker='x')
plt.plot(look_sequence, label='LOOK', marker='^')
plt.plot(lfu_sequence, label='LFU', marker='s')
plt.xlabel('Sequence Number')
plt.ylabel('Total Seek Time (ms)')
plt.title('Disk Scheduling Algorithms - Total Seek Time')
plt.legend()
plt.grid(True)
plt.show()
