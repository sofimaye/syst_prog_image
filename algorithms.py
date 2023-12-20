import random
import time
class DiskScheduler:
    def __init__(self, tracks=500, sectors_per_track=100, current_track=0, track_seek_time=10, rotation_delay=8):
        self.tracks = tracks
        self.sectors_per_track = sectors_per_track
        self.current_track = current_track
        self.track_seek_time = track_seek_time
        self.rotation_delay = rotation_delay

    def calculate_seek_time(self, track):
        seek_distance = abs(self.current_track - track)
        return seek_distance * self.track_seek_time + self.rotation_delay

    def fcfs(self, request_queue):
        total_time = 0
        for track in request_queue:
            total_time += self.calculate_seek_time(track)
            self.current_track = track
        return total_time

    def sstf(self, request_queue):
        total_time = 0
        while request_queue:
            next_track = min(request_queue, key=lambda track: abs(self.current_track - track))
            total_time += self.calculate_seek_time(next_track)
            self.current_track = next_track
            request_queue.remove(next_track)
        return total_time

    def look(self, request_queue):
        total_time = 0
        direction = 1  # 1 for moving towards outer tracks, -1 for inner tracks
        while request_queue:
            if direction == 1:
                next_track = min([track for track in request_queue if track > self.current_track], default=None)
                if next_track is None:
                    direction = -1
                    continue
            else:
                next_track = max([track for track in request_queue if track < self.current_track], default=None)
                if next_track is None:
                    direction = 1
                    continue
            total_time += self.calculate_seek_time(next_track)
            self.current_track = next_track
            request_queue.remove(next_track)
        return total_time

    def lfu(self, request_queue, num_segments=3):
        total_time = 0
        segments = [[] for _ in range(num_segments)]
        segment_counters = [{} for _ in range(num_segments)]

        for track in request_queue:
            segment_idx = track % num_segments
            if track in segment_counters[segment_idx]:
                segment_counters[segment_idx][track] += 1
            else:
                segment_counters[segment_idx][track] = 1
            segments[segment_idx].append(track)

        while request_queue:
            segment_idx = request_queue[0] % num_segments
            min_count = float('inf')
            min_track = None

            for track, count in segment_counters[segment_idx].items():
                if count < min_count:
                    min_count = count
                    min_track = track

            if min_track is None:
                segment_counters[segment_idx] = {}
                segment_idx = (segment_idx + 1) % num_segments
                continue

            total_time += self.calculate_seek_time(min_track)
            self.current_track = min_track
            request_queue.remove(min_track)
            segments[segment_idx].remove(min_track)
            del segment_counters[segment_idx][min_track]

        return total_time

class FileSystem:
    def __init__(self, disk_scheduler, max_requests=20, buffer_cache_size=250):
        self.disk_scheduler = disk_scheduler
        self.files = {}  # Dictionary to store files and their blocks on disk
        self.max_requests = max_requests
        self.buffer_cache = {}  # Cache for blocks
        self.buffer_cache_size = buffer_cache_size
        self.current_requests = 0
    def create_file(self, filename, num_blocks):
        if filename in self.files:
            raise Exception(f"File '{filename}' already exists.")
        self.files[filename] = [None] * num_blocks

    def write_block(self, filename, block_num, data):
        if filename not in self.files:
            raise Exception(f"File '{filename}' does not exist.")
        if block_num >= len(self.files[filename]) or block_num < 0:
            raise Exception(f"Invalid block number {block_num} for file '{filename}'.")
        self.files[filename][block_num] = data
        self.buffer_cache[(filename, block_num)] = data  # Adding to cache

    def read_block(self, filename, block_num):
        if filename not in self.files:
            raise Exception(f"File '{filename}' does not exist.")
        if block_num >= len(self.files[filename]) or block_num < 0:
            raise Exception(f"Invalid block number {block_num} for file '{filename}'.")
        return self.buffer_cache.get((filename, block_num), None) or self.files[filename][block_num]

    def process_request(self, process):
        if self.current_requests < self.max_requests:
            self.current_requests += 1
            process.run()
            self.current_requests -= 1
        else:
            print("Перевищено максимальну кількість запитів.")


class Process:
    def __init__(self, file_system, file_name, num_blocks, max_requests, process_time=20):
        self.file_system = file_system
        self.file_name = file_name
        self.num_blocks = num_blocks
        self.max_requests = max_requests
        self.process_time = process_time  # Квант часу (мс)

    def run(self):
        start_time = time.time()
        while (time.time() - start_time) * 1000 < self.process_time:
            block_num = random.randint(0, self.num_blocks - 1)
            if random.random() < 0.5:  # 50% ймовірність читання або запису
                self.file_system.write_block(self.file_name, block_num, f"Data for block {block_num}")
            else:
                self.file_system.read_block(self.file_name, block_num)


# Тестування алгоритмів і файлової системи
disk_scheduler = DiskScheduler()
file_system = FileSystem(disk_scheduler, max_requests=20, buffer_cache_size=250)

# Створення файлів для процесів
for i in range(10):  # 10 процесів
    file_name = f"file{i}.txt"
    num_blocks = random.choice([10, 150, 500])  # Малі, середні або великі файли
    file_system.create_file(file_name, num_blocks=num_blocks)

    # Створення і запуск процесу
    process = Process(file_system, file_name, num_blocks, max_requests=20, process_time=20)
    file_system.process_request(process)

# Отримання та виведення результатів алгоритмів планування
request_queue = [143, 86, 147, 91, 171, 19, 62, 96]
fcfs_time = disk_scheduler.fcfs(request_queue.copy())
sstf_time = disk_scheduler.sstf(request_queue.copy())
look_time = disk_scheduler.look(request_queue.copy())
lfu_time = disk_scheduler.lfu(request_queue.copy(), num_segments=3)

request_queue2 = [62, 96, 34, 1000, 567, 15, 16, 250]
fcfs_time1 = disk_scheduler.fcfs(request_queue2.copy())
sstf_time1 = disk_scheduler.sstf(request_queue2.copy())
look_time1 = disk_scheduler.look(request_queue2.copy())
lfu_time1 = disk_scheduler.lfu(request_queue2.copy(), num_segments=3)


request_queue3 = [62, 96, 34, 1000, 567, 15, 16, 250]
fcfs_time3 = disk_scheduler.fcfs(request_queue3.copy())
sstf_time3 = disk_scheduler.sstf(request_queue3.copy())
look_time3 = disk_scheduler.look(request_queue3.copy())
lfu_time3 = disk_scheduler.lfu(request_queue3.copy(), num_segments=3)


print(f"FCFS Time: {fcfs_time} ms")
print(f"SSTF Time: {sstf_time} ms")
print(f"LOOK Time: {look_time} ms")
print(f"LFU Time: {lfu_time} ms")
print("__________________________________")
print(f"FCFS Time: {fcfs_time1} ms")
print(f"SSTF Time: {sstf_time1} ms")
print(f"LOOK Time: {look_time1} ms")
print(f"LFU Time: {lfu_time1} ms")
print("__________________________________")
print(f"FCFS Time: {fcfs_time3} ms")
print(f"SSTF Time: {sstf_time3} ms")
print(f"LOOK Time: {look_time3} ms")
print(f"LFU Time: {lfu_time3} ms")
