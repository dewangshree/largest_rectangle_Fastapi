from typing import Optional


def _largest_histogram(heights: list[int]) -> int:
    """Returns the area of the largest rectangle in a histogram."""
    stack: list[int] = []
    max_area = 0

    for i in range(len(heights) + 1):
        curr_h = heights[i] if i < len(heights) else 0

        while stack and heights[stack[-1]] > curr_h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)

        stack.append(i)

    return max_area


def largest_rectangle(matrix: list[list[int]]) -> tuple[Optional[int], int]:
    """
    Finds the value that forms the largest rectangle of identical
    elements in a 2D matrix.

    Args:
        matrix: A 2D list of integers with uniform row lengths.

    Returns:
        A tuple of (value, area) for the largest uniform rectangle found.
        Returns (None, 0) if the matrix is empty.

    Raises:
        ValueError: If matrix rows have unequal lengths.
    """
    if not matrix or not matrix[0]:
        return (None, 0)

    if len({len(row) for row in matrix}) > 1:
        raise ValueError("All rows must have the same length.")

    unique_vals = {val for row in matrix for val in row}
    best_num: Optional[int] = None
    best_area = 0

    for num in unique_vals:
        heights = [0] * len(matrix[0])

        for row in matrix:
            heights = [h + 1 if val == num else 0 for h, val in zip(heights, row)]
            area = _largest_histogram(heights)

            if area > best_area:
                best_area = area
                best_num = num

    return (best_num, best_area)