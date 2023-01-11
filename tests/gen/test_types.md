# Test Types

## find-one

Given an image and a template, find a bounding box that (approximately) matches the template, or report that none exists.

If multiple templates exist in the image, matching any one of them counts as a pass.

The tester has a small error tolerance for the bounding box (12.5% relative, 15 pixels absolute).