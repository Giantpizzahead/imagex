# Goals

What the outward-facing API of the ImageX module should be able to do.

## Test Format

The `resources` directory contains all the images and templates used during testing. They can be in subdirectories.

Each of the separate goals will be in its own directory.

Each directory will have a `test.py` file that runs the tests for that goal.

There may be multiple subdirectories in each of the goal directories. These should be used to group tests with similar difficulties and/or generation methods.

Each `.json` file corresponds to one test. The parameters of the test should be in this json file (whatever that means for each specific goal).

We should also create a `benchmark.py` file that displays the speed of each type of task, varying based on template and image sizes or edge cases.

`context.py` can contain helpful setup functions for testing.

The main test directory will also have a `test.py`, where one can manually turn on/off the specific test categories.

## 1. Find the exact template itself

Label: find-identity

Given two copies of the same image, ImageX should be able to locate the bounding box of the image.

Example:
```python
import imagex

image = imagex.Image("path/to/template.png")
template = imagex.Image("path/to/template.png")

result = imagex.find(template, image)
# Check that the bounding box is within an acceptable
# distance from the correct bounding box
```

## 2. Find the exact template in a larger image

Label: find-copy-exact

Given an image containing the exact template (same pixels), find the template's bounding box.

## 3. Exact match with noise

Label: find-copy-noise

Given an image containing the exact template, but with a bit of noise applied, find the template's bounding box.

The noise amount should be such that a human can still easily see the template. It can be any type of noise (lighting, random, etc). This definition holds for future goals as well.

## 4. Avoid false positives

Label: find-no-false-positives

Given an image that does not contain the template (or anything similar), ImageX should not output a bounding box.

For all test images and templates, a human should be able to easily see that the template is not in the image.

Tests in this category should be very obvious to both humans and computers, with no room for disputes.

## 5. Avoid near positives (Subjective)

Label: find-no-near-positives

Given an image that does not contain the template, but contains something that looks similar, ImageX should not output a bounding box.

For all test images and templates, a human should be able to easily see that the template is not in the image. However, computers might have a harder time.

This category is subjective, so it's ok if not all tests pass.

## 6. Scale-invariant match

Label: find-scaled-exact

Given an image containing a scaled version of the template, but with no extra noise applied, find the template's bounding box.

## 7. Scale-invariant match with noise (CAPSTONE 1)

Label: find-scaled-noise

**This goal should pass without any new features.**

Same as 6, but with noise.

## 8. Rotation-invariant match

Label: find-rotated-exact

Given an image containing a rotated version of the template, but with no scaling or extra noise applied, find the template's bounding box.

## 9. Rotation-invariant match with noise

Label: find-rotated-noise

**This goal should pass without any new features.**

Same as 8, but with noise.

## 10. Flip-invariant match

Label: find-flipped-and-rotated

Given an image containing a flipped and/or rotated version of the template, but with no scaling or extra noise applied, find the template's bounding box.

## 11. Transformed match

Label: find-transformed-exact

**This goal should pass without any new features.**

Given an image containing a transformed version of the template (scaled, rotated, flipped, translated), but with no extra noise applied, find the template's bounding box.

## 12. Transformed match with noise (CAPSTONE 2)

Label: find-transformed-noise

**This goal should pass without any new features.**

Same as 11, but with noise.

# Bonus Goals

These would be cool, but would also probably take a lot more work and make the library slower overall. They also have less use cases.

## 13. Match with obstructions

Label: find-obstructed-exact

Given an image containing an exact copy of the template (no transformations), but with up to 80% of the template obstructed, find the template's bounding box.

The template should still be easily located by a human.

## 14. Match with obstructions and noise

Label: find-obstructed-noise

**This goal should pass without any new features.**

Same as 13, but with noise.

## 15. Match with transparency

Label: find-transparent-exact

Allow the template to have transparency; an alpha value of 0 should be treated as a transparent pixel, and should not affect the matching result.

## 16. Match with transparency and noise

Label: find-transparent-noise

**This goal should pass without any new features.**

Same as 15, but with noise.

## 17. General 2D matching: Positive (CAPSTONE 3)

Label: find-2d-positive

**This goal should pass without any new features.**

Cumulative test for all previous goals, where the template is included in the image (in some manner).

Tests in this category should be very obvious to both humans and computers, with no room for disputes.

## 18. General 2D matching: Negative

Label: find-2d-negative

**This goal should pass without any new features.**

Cumulative test for all previous goals, where the template is not present in the image.

Tests in this category should be very obvious to both humans and computers, with no room for disputes.

## 19. General 2D matching: Boundary (Subjective)

Label: find-2d-boundary

Cumulative test for all previous goals, containing a mix of hard-to-call cases.

A human should be able to easily identify whether the template is in the image. However, computers might have a harder time.

This category is subjective, so it's ok if not all tests pass.

## 20. Multiple matches without overlap

Label: find-multiple-separated-exact

Given an image containing multiple copies of the exact template, without transformations, noise, or overlaps, find all of the bounding boxes.

## 21. Multiple matches without overlap (general)

Label: find-multiple-separated-general

**This goal should pass without any new features.**

Given an image containing multiple copies of the template, with transformations and noise, but no overlap, find all of the bounding boxes.

## 22. Multiple matches with overlaps

Label: find-multiple-overlapping-exact

Given an image containing multiple copies of the exact template, without transformations or noise, but with up to 75% overlap (up to 75% of any single template area is shared with any other template), find all of the bounding boxes.

## 23. General 2D matching: Multiple matches (CAPSTONE 4)

Label: find-2d-multiple

Cumulative test for all previous goals, containing multiple matches.

## 24. 3D mesh matching

Label: find-mesh-exact

Given a 3D mesh, created using some 3D modeler, find an exact copy of some side of the mesh in an image (in other words, what the mesh would look like when projected onto some 2D plane), and output a bounding box.

## 25. 3D mesh matching with noise

Label: find-mesh-noise

**This goal should pass without any new features.**

Same as 24, but with noise.

## 26. General 3D matching: Positive (CAPSTONE 5)

Label: find-3d-positive

Cumulative positive test for all 3D-related goals.

## 27. General 3D matching: Negative

Label: find-3d-negative

Cumulative negative test for all 3D-related goals.

## 28. General 3D matching: Boundary (Subjective)

Label: find-3d-boundary

Cumulative subjective test for all 3D-related goals.
