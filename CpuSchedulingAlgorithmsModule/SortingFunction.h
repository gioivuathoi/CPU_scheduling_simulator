#ifndef __COMPARE__FUNCTION__
#define __COMPARE__FUNCTION__

// Sorting Function

/* Khai báo tiêu đề tuỳ chỉnh  */
#include "./Process.h"

/**
 * [compare_by_return_time Khai báo hàm so sánh dựa trên thời gian trả về]
 * @param  a [Cấu trúc tiến trình 1]
 * @param  b [Cấu trúc tiến trình 2]
 * @return   [Kết quả so sánh]
 */
int compare_by_return_time(const void *a, const void *b)
{
	/* Ép kiểu biến sang dạng const void */
	Process *ptA = (Process *)a;
	Process *ptB = (Process *)b;

	/* Trong trường hợp thời gian trả về của ptA nhỏ hơn, */
	if (ptA->return_time < ptB->return_time)
		return -1;
		// Trả về -1

	/* Trong trường hợp thời gian trả về của ptA lớn hơn, */
	else if (ptA->return_time > ptB->return_time)
		return 1;
		// Trả về 1

	/* Trong trường hợp thời gian trả về bằng nhau */
	else
		return 0;
		// Trả về 0 
}

/**
 * [quick_sort_by_return_time Hàm sắp xếp nhanh theo thời gian trả về]
 * @param p   [Mảng cấu trúc tiến trình]
 * @param len [Số lượng tiến trình]
 */
void quick_sort_by_return_time(Process p[], int len)
{
	qsort(p, len, sizeof(Process), compare_by_return_time);
	// Gọi hàm qsort, sử dụng hàm so sánh compare_by_return_time để so sánh thời gian trả về.
}

/**
 * [merge Hàm hợp nhất các mảng đã chia]
 * @param arr   [Mảng cần sắp xếp]
 * @param left  [Chỉ số bên trái của mảng]
 * @param mid   [Chỉ số giữa của mảng]
 * @param right [Chỉ số bên phải của mảng]
 */
void merge(Process arr[], int left, int mid, int right)
{
	int fIdx = left;
	// Khai báo và khởi tạo biến để lưu trữ chỉ số bắt đầu của mảng bên trái
	int rIdx = mid + 1;
	// Khai báo và khởi tạo biến để lưu trữ chỉ số bắt đầu của mảng bên phải
	int i;
	// Khai báo biến sử dụng trong vòng lặp

	Process *sortArr = (Process *)malloc(sizeof(Process) * (right + 1));
	// Cấp phát bộ nhớ động để lưu trữ mảng đã sắp xếp
	int sIdx = left;

	/* So sánh các khối từ left đến mid và từ mid + 1 đến right */
	while (fIdx <= mid && rIdx <= right)
	{
		/* Trường hợp thời gian đến của left nhỏ hơn thời gian đến của right */
		if (arr[fIdx].arrive_time <= arr[rIdx].arrive_time)
			sortArr[sIdx] = arr[fIdx++];
			// Sao chép dữ liệu của left vào mảng kết quả

		/* Trong trường hợp ngược lại */
		else
			sortArr[sIdx] = arr[rIdx++];
			// Sao chép dữ liệu của right vào mảng kết quả

		sIdx++;
		// Tăng chỉ số mảng kết quả lên
	}

	/* Trong trường hợp còn dữ liệu trong mảng bên phải */
	if (fIdx > mid)
	{
		/* Lặp lại cho đến khi hết dữ liệu */
		for (i = rIdx; i <= right; i++, sIdx++)
			sortArr[sIdx] = arr[i];
			// Sao chép dữ liệu của mảng bên phải vào mảng kết quả
	}

	/* Trong trường hợp còn dữ liệu trong mảng bên trái */
	else
	{
		/* Lặp lại cho đến khi hết dữ liệu */
		for (i = fIdx; i <= mid; i++, sIdx++)
			sortArr[sIdx] = arr[i];
			// Sao chép dữ liệu của mảng bên trái vào mảng kết quả
	}

	/* Lặp lại theo số lượng phần tử trong mảng */
	for (i = left; i <= right; i++)
		arr[i] = sortArr[i];
		// Sao chép mảng gốc

	free(sortArr);
	// Giải phóng bộ nhớ đã cấp phát cho mảng
}

/**
 * [Gọi hàm merge_sort_by_arrive_time để thực hiện sắp xếp trộn dựa trên thời gian đến]
 * @param arr   [Mảng cần sắp xếp]
 * @param left  [Chỉ số bên trái của mảng]
 * @param right [Chỉ số bên phải của mảng]
 */
void merge_sort_by_arrive_time(Process arr[], int left, int right)
{
	int mid;
	// Khai báo biến để lưu trữ chỉ số trung tâm

	/* Nếu chỉ số bên trái nhỏ hơn chỉ số bên phải */
	if (left < right)
	{
		/* Tính chỉ số trung tâm */
		mid = (left + right) / 2;

		/* Chia mảng thành hai phần và sắp xếp mỗi phần */
		merge_sort_by_arrive_time(arr, left, mid);
		merge_sort_by_arrive_time(arr, mid + 1, right);

		/* Hợp nhất hai mảng đã sắp xếp */
		merge(arr, left, mid, right);
	}
}

#endif
